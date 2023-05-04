using System.Windows;
using MahApps.Metro.Controls;
using Newtonsoft.Json;
using MahApps.Metro.Controls.Dialogs;
using Bogus;
using FakeIotDevice.Models;
using uPLibrary.Networking.M2Mqtt;
using System.Threading;
using System.Diagnostics;
using System.Text;
using System;
using System.Windows.Documents;

namespace FakeIotDevice
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        Faker<SensorInfo> FakeHomeSensor { get;set; } = null; // 가짜 스마트홈 센서값
        MqttClient Client { get; set; }
        Thread MqttThread { get; set; }

        public MainWindow()
        {
            InitializeComponent();
            InitFakeData();
        }

        private void InitFakeData()
        {
            var Rooms = new[] { "Bed", "Bath", "Living", "Dining" };
            FakeHomeSensor = new Faker<SensorInfo>()
                .RuleFor(s => s.Home_Id, "D101H703") // 임의로 픽스된 홈 아이디 101동 703호
                .RuleFor(s => s.Room_Name, f => f.PickRandom(Rooms)) // 실행할때마다 방이름이 계속 변경
                .RuleFor(s => s.Sensing_DateTime, f => f.Date.Past(0)) // 현재시각이 생성
                .RuleFor(s => s.Temp, f => f.Random.Float(20.0f, 30.0f)) // 20~30도 사이의 실수값 생성
                .RuleFor(s => s.Humid, f => f.Random.Float(40.0f, 64.0f)); // 40~64% 사이의 습도값
        }

        private async void BtnConnect_Click(object sender, RoutedEventArgs e)
        {
            if(string.IsNullOrEmpty(TxtMqttBrokerIp.Text))
            {
                await this.ShowMessageAsync("오류", "브로커 아이피를 입력하세요");
                return;
            }
            // 브로커아이피로 접속
            ConnectMqttBroker();

            //하위 로직 무한반복
            StartPublish();

            // 가짜 스마트홈 센서값 생성

            // 센서값 MQTT 브로커에 전송

            // RtbLog에 접속
        }
        // 핵심처리 센싱된 데이터값을 MQTT 브로커로 전송
        private void StartPublish()
        {
            MqttThread = new Thread(() =>
            {
                while (true)
                {
                    //가짜 스마트홈 센서값 생성
                    SensorInfo Info = FakeHomeSensor.Generate();
                    //릴리즈(배포) 시 주석처리 
                    Debug.WriteLine($"{Info.Home_Id} / {Info.Room_Name} / {Info.Sensing_DateTime} / {Info.Temp}");
                    // 객체 직렬화(객체데이터를 xml이나 json등의 문자열로 변환)
                    var jsonValue = JsonConvert.SerializeObject(Info, Formatting.Indented);
                    // 센서값 MQTT 브로커에 전송(Publish)
                    Client.Publish("SmartHome/IotData/", Encoding.Default.GetBytes(jsonValue));
                    //Thread , UI Thread 충돌 안나도록 변경
                    this.Invoke(new Action(delegate ()
                    {
                        RtbLog.AppendText($"{jsonValue}\n");
                        RtbLog.ScrollToEnd();
                    }));
                    
                    //1초동안 대기
                    Thread.Sleep(1000);
                }
            });
            MqttThread.Start();
        }

        private void ConnectMqttBroker()
        {
            Client = new MqttClient(TxtMqttBrokerIp.Text);
            Client.Connect("SmartHomeDev");//publish Client ID를 지정
        }

        // 접속 끊지 않으면 메모리상에 계속 남아있는 경우 발생
        private void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (Client != null && Client.IsConnected == true)
            {
                Client.Disconnect();//접속끊음
            }
            if(MqttThread!=null)
            {
                MqttThread.Abort();//Abort로 접속을 끊어주지 않으면 프로그램 종료 후에도 메모리에 남아있음
            }
        }

        private void MetroWindow_Loaded(object sender, RoutedEventArgs e)
        {
            TxtMqttBrokerIp.Focus();
        }
    }
}
