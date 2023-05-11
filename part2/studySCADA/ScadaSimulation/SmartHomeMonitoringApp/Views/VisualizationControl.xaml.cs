using LiveCharts;
using LiveCharts.Wpf;
using MySql.Data.MySqlClient;
using SmartHomeMonitoringApp.Logics;
using SmartHomeMonitoringApp.Models;
using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web.Configuration;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// VisualizationControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class VisualizationControl : UserControl
    {
        List<string> Divisions = null;
        string FirstSensingDate = string.Empty;
        int TotalDataCount = 0;//검색된 데이터 개수

        public VisualizationControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            //룸선택 콤보박스 초기화
            Divisions = new List<string> {"SELECT","LIVING","DINING","BED","BATH"};
            CboRoomName.ItemsSource = Divisions;
            CboRoomName.SelectedIndex = 0;

            //검색시작일 날짜 - DB에서 제일 오래된 날짜를 받아옴
            using(MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
            {
                conn.Open();
                var dtQuery = @"SELECT F.Sensing_Date
                                  FROM (
                                   SELECT DATE_FORMAT(Sensing_DateTime, '%Y-%m-%d') AS Sensing_Date
                                      FROM smarthomesensor
                                ) AS F
                                 GROUP BY F.Sensing_Date
                                 ORDER BY F.Sensing_Date ASC Limit 1;";
                MySqlCommand cmd = new MySqlCommand(dtQuery, conn);
                var result = cmd.ExecuteScalar();
                //Debug.WriteLine(result.ToString());
                FirstSensingDate =DtpStart.Text= result.ToString();
                // 검색종료일은 현재일자를 할당
                DtpEnd.Text = DateTime.Now.ToString("yyyy-MM-dd");
            }
        }
        //검색버튼 클릭 이벤트 핸들러
        private async void BtnSearch_Click(object sender, RoutedEventArgs e)
        {
            bool IsValid = true;
            string errorMsg = string.Empty;
            DataSet ds = new DataSet();
            // Validation Check
            if (CboRoomName.SelectedValue.ToString() == "SELECT")
            {
                IsValid = false;
                errorMsg += "방 구분을 선택하세요.\n";
            }
            // 시작 날짜보다 더 이른 날짜로 검색하려고 하면
            if(DateTime.Parse(DtpStart.Text)<DateTime.Parse(FirstSensingDate))
            {
                IsValid=false;
                errorMsg += $"검색 시작일은 {FirstSensingDate} 부터 가능합니다!\n";
            }
            // 오늘 날짜 이후 날짜 검색 시 
            if(DateTime.Parse(DtpEnd.Text) > DateTime.Now)
            {
                IsValid = false;
                errorMsg += "검색 종료일은 오늘까지 가능합니다\n!";
            }
            //검색 시작일이 검색 종료일보다 이후인 경우
            if(DateTime.Parse(DtpStart.Text) > DateTime.Parse(DtpEnd.Text))
            {
                IsValid = false;
                errorMsg += "검색 시작일이 검색 종료일보다 최신일 수 없습니다!\n";
            }
            if(IsValid==false)
            {
                await Commons.ShowCustomMessageAsync("검색", errorMsg);
                return;
            }

            // 검색
            TotalDataCount = 0;
            try
            {
                using(MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                {
                    conn.Open();
                    var searchQuery = @"SELECT id,
		                                Home_Id,
		                                Room_Name,
		                                Sensing_DateTime,
		                                Temp,
		                                Humid
                                 FROM smarthomesensor
                                WHERE UPPER(Room_Name) = @Room_Name
                                 AND DATE_FORMAT(Sensing_DateTime,'%Y-%m-%d') 
                                BETWEEN @StartDate AND @EndDate";
                    MySqlCommand cmd = new MySqlCommand(searchQuery, conn);
                    cmd.Parameters.AddWithValue("@Room_Name", CboRoomName.SelectedValue.ToString());
                    cmd.Parameters.AddWithValue("@startDate", DtpStart.Text);
                    cmd.Parameters.AddWithValue("@EndDate", DtpEnd.Text);
                    MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);
                    adapter.Fill(ds, "smarthomesensor");
                    //MessageBox.Show(ds.Tables["smarthomesensor"].Rows.Count.ToString(),"TotalData"); //데이터 개수 확인
                }
            }
            catch (Exception ex)
            {
                await Commons.ShowCustomMessageAsync("DB검색", $"DB검색 오류 {ex.Message}");
            }

            //DB에서 가져온 데이터를 차트에 뿌리는 부분
            if (ds.Tables[0].Rows.Count > 0)
            {
                foreach (DataRow row in ds.Tables[0].Rows)
                {
                    Convert.ToDouble(row["Temp"]);
                }
            }
        }
    }
}
