using System;
using System.Windows.Forms;

namespace Sensores
{
    internal static class Program
    {
        /// <summary>
        /// Punto de entrada principal para la aplicación.
        /// </summary>
        
        public static IP UI = null;

        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Program.UI = new IP(args);
            Application.Run(Program.UI);
        }
    }
}
