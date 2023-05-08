using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DataBaseControl : UserControl
    {
        public bool isConnected { get; set; }

        public DataBaseControl()
        {
            InitializeComponent();
        }
        // 유저컨트롤 로드 이벤트 핸들러
        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnString.Text = Commons.MYSQL_CONNSTRING;

            isConnected = false;
            BtnConnDb.IsChecked = false;
        }
        //토글버튼 클릭이벤트 핸들러
        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
            if (isConnected == false)
            {
                BtnConnDb.IsChecked = true;
                isConnected = true;
                //MQTT 브로커에 접속
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);
                try
                {
                    //Mqtt subscribe(구독할) 로직 처리
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {
                        //Mqtt 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR");//clientId = 모니터
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                            new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });
                        UpdateLog(">>> MQTT Broker Connected");
                        BtnConnDb.IsChecked = true;
                        isConnected = true;
                    }
                }
                catch
                {
                    // Pass
                }
            }
            else
            {
                BtnConnDb.IsChecked = false;
                isConnected = false;
            }
        }

        private void UpdateLog(string msg)
        {
            //예외처리 필요
            this.Invoke(()=>{
                TxtLog.Text += $"{msg}\n";
                TxtLog.ScrollToEnd();
            });
        }
        //Subscribe가 발생할 때 이벤트 핸들러
        private void MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            UpdateLog(msg);
            SetToDataBase(msg, e.Topic);//실제 DB에 저장
        }

        //DB 저장처리 메서드
        private void SetToDataBase(string msg, string topic)
        {
            var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
            if(currValue != null)
            {
                //Debug.WriteLine(currValue["Home_Id"]);
                //Debug.WriteLine(currValue["Room_Name"]);
                //Debug.WriteLine(currValue["Sensing_DateTime"]);
                //Debug.WriteLine(currValue["Temp"]);
                //Debug.WriteLine(currValue["Humid"]);
                try
                {
                    using(MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                    {
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string insQuery = "INSERT INTO smarthomesensor ... ";
                        MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                        cmd.Parameters.AddWithValue("@Home_Id", currValue["Home_Id"]);
                        // ... 파라미터 5개
                        if(cmd.ExecuteNonQuery()==1)
                        {
                            UpdateLog(">>> DB Insert 성공");
                        }
                        else
                        {
                            UpdateLog(">>> Db Insert 실패");
                        }
                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!! Error 발생 : {ex.Message}");
                }
            }
        }
    }
}
