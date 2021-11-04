using System;
using System.Drawing;
using System.Windows.Forms;

namespace Sensores
{
    public partial class IP : Form
    {
        public string[] args;

        public IP(string[] args)
        {
            this.args = args;
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            foreach (string arg in args)
            {
                if (arg.StartsWith("--ip="))
                {
                    IPValue.Text = arg.Substring(arg.IndexOf('=') + 1);
                } 
                else if (arg.StartsWith("--port="))
                {
                    PortValue.Value = int.Parse(arg.Substring(arg.IndexOf('=') + 1));
                }
                else if (arg.StartsWith("--id="))
                {
                    SensorId.Text = arg.Substring(arg.IndexOf('=') + 1);
                }
            }
        }

        private void ValueBeingSent_ValueChanged(object sender, EventArgs e)
        {
            Sensor.Population = (int)((NumericUpDown)sender).Value;
        }

        private void Conectar_Click(object sender, EventArgs e)
        {
            try
            {
                AddMessageToLog("Intentando conectar al servidor " + IPValue.Text + " y al puerto " + PortValue.Value, 3);
                Sensor.InitializeKafkaServers(IPValue.Text, (int)PortValue.Value);
                RunStatus(false);
            }
            catch (Exception)
            {
                AddMessageToLog("No se ha podido establecer comunicación con el servidor", 0);
            }
        }

        private void Desconectar_Click(object sender, EventArgs e)
        {
            try
            {
                AddMessageToLog("Desconectando del servidor...", 1);
                RunStatus(true);
            }
            catch (Exception)
            {
                AddMessageToLog("Se ha producido un error cuando se cerraba la comunicación con el servidor", 0);
            }
        }

        private void RunStatus(bool status)
        {
            IPValue.Enabled = status;
            PortValue.Enabled = status;
            SensorId.Enabled = status;

            Conectar.Enabled = status;
            Desconectar.Enabled = !status;

            Temporizador.Enabled = !status;
            if (Temporizador.Enabled)
            {
                AddMessageToLog("Se ha activado el temporizador", 1);
            }
            else
            {
                AddMessageToLog("Se ha desactivado el temporizador", 3);
            }
        }

        public void AddMessageToLog(string message, int type)
        {
            Label aux = new Label
            {
                Text = message,
                Font = new Font("Microsoft Sans Serif", 10, FontStyle.Regular),
                AutoSize = true,
                Dock = DockStyle.Bottom,
            };

            if (type == 0) // ERROR
            {
                aux.ForeColor = Color.FromArgb(220, 53, 69);
            }
            else if (type == 1) // INFO
            {
                aux.ForeColor = Color.FromArgb(23, 162, 184);
            }
            else if (type == 2) // SUCCESS
            {
                aux.ForeColor = Color.FromArgb(40, 167, 69);
            }
            else
            {
                aux.ForeColor = Color.FromArgb(255, 193, 7);
            }

            this.Logs.Controls.Add(aux);
            this.Logs.VerticalScroll.Value = this.Logs.VerticalScroll.Maximum;
        }

        private void Temporizador_Tick(object sender, EventArgs e)
        {
            AddMessageToLog("Se va a intentar enviar información al servidor", 1);
            Sensor.EnviarInfo();
        }

        private void SensorId_TextChanged(object sender, EventArgs e)
        {
            Sensor.SensorId = SensorId.Text;
        }
    }
}
