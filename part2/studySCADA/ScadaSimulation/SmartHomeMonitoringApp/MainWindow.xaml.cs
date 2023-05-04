using System;
using System.Collections.Generic;
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
using MahApps.Metro.Controls;
using SmartHomeMonitoringApp.Views;
using System.Diagnostics;

namespace SmartHomeMonitoringApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void MetroWindow_Loaded(object sender, RoutedEventArgs e)
        {
            // <Frame> -> '페이지'로 만들고
            // <ContentControl> -> '사용자 정의 컨트롤로 만듬
            // 즉 ContentControl로 만들면 다른 곳에서 편하게 불러다 사용가능
            ActiveItem.Content=new Views.DataBaseControl(); 
        }
        //끝내기
        private void MnuExitProgram_Click(object sender, RoutedEventArgs e)
        {
            System.Diagnostics.Process.GetCurrentProcess().Kill();//작업관리자에서 프로그램 종료와 같은 역할
            Environment.Exit(0); //40행,41행 둘중 하나만 쓰면됨
        }
    }
}
