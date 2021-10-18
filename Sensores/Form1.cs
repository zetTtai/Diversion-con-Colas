using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Sensores
{
    public partial class IP : Form
    {
        public IP()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
        }

        private void ValueBeingSent_ValueChanged(object sender, EventArgs e)
        {
            Sensor.Population = (int)((NumericUpDown)sender).Value;
        }

        private void Conectar_Click(object sender, EventArgs e)
        {
            try
            {
                AddMessageToLog("Intentando conectar al servidor " + IPValue.Text + " y al puerto " + PortValue.Value, 1);
                Sensor.ProbarConexion();
                RunStatus(false);
                Sensor.ChangeServer(IPValue.Text);
                Sensor.ChangePort((int)PortValue.Value);
            }
            catch (Exception)
            {
                AddMessageToLog("No se ha podido establecer comunicación con el servidor", 3);
            }
        }

        private void Desconectar_Click(object sender, EventArgs e)
        {
            try
            {
                AddMessageToLog("Desconectando del servidor...", 1);
                Sensor.ChangeServer("");
                Sensor.ChangePort(0);
                RunStatus(true);
            }
            catch (Exception)
            {
                AddMessageToLog("Se ha producido un error cuando se cerraba la comunicación con el servidor", 3);
            }
        }

        private void RunStatus(bool status)
        {
            IPValue.Enabled = status;
            PortValue.Enabled = status;
            Temporizador.Enabled = status;
        }

        public void AddMessageToLog(string message, int type)
        {
            Label aux = new Label
            {
                Text = message,
                Font = new Font("Microsoft Sans Serif", 10, FontStyle.Regular),
                AutoSize = true,
                Location = new Point(10, 25 * Logs.Controls.Count)
            };

            if (type == 0)
            {
                aux.ForeColor = Color.FromArgb(220, 53, 69);
            }
            else if (type == 1)
            {
                aux.ForeColor = Color.FromArgb(23, 162, 184);
            }
            else if (type == 2)
            {
                aux.ForeColor = Color.FromArgb(40, 167, 69);
            }
            else
            {
                aux.ForeColor = Color.FromArgb(255, 193, 7);
            }

            Thread.Sleep(100);
            this.Logs.Controls.Add(aux);
        }

        private void Temporizador_Tick(object sender, EventArgs e)
        {
            Sensor.EnviarInfo();
        }
    }
}
