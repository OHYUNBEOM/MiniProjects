using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using uPLibrary.Networking.M2Mqtt;

namespace SmartHomeMonitoringApp.Logics
{
    public class Commons
    {
        // 화면마다 공유할 MQTT 브로커 IP
        public static string BROKERHOST { get; set; } = "127.0.0.1";

        public static string MQTTTOPIC { get; set; } = "SmartHome/IotData/";

        public static string MYSQL_CONNSTRING { get; set; } = "Server=localhost;" +
                                                "Port=3306;" +
                                                "Database=miniproject;" +
                                                "Uid=root;" +
                                                "Pwd=12345;";
        //MQTT 클라이언트 공용 객체
        public static MqttClient MQTT_CLIENT { get; set; }

        // 비동기 매세지 창 사용하기 위함
        public static async Task<MessageDialogResult> ShowCustomMessageAsync(string title, string message,
            MessageDialogStyle style=MessageDialogStyle.Affirmative)
        {
            return await ((MetroWindow)Application.Current.MainWindow).ShowMessageAsync(title, message, style, null);
        }
    }
}
