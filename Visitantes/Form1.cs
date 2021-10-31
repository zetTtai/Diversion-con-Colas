using System;
using System.Drawing;
using System.Windows.Forms;
using Confluent.Kafka;

namespace Visitantes
{
    public partial class Form1 : Form
    {

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            int PanelSize = Mapa.Width / 20;

            for (int i = 0; i < 20; i++)
            {
                for (int j = 0; j < 20; j++)
                {

                    Panel aux = new Panel
                    {
                        Location = new Point(PanelSize * j, PanelSize * i),
                        Width = PanelSize,
                        Height = PanelSize,
                        Name = "{$i},{$j}",
                        BackColor = Color.FromArgb(1303030),
                        BorderStyle = BorderStyle.FixedSingle,
                    };
                    Mapa.Controls.Add(aux);
                }
            }
        }

        private void Conectar_Click(object sender, EventArgs e)
        {

        }

        private void Desconectar_Click(object sender, EventArgs e)
        {

        }

        private void Temporizador_Tick(object sender, EventArgs e)
        {
            ActualizarMapa();
        }

        private void ActualizarMapa()
        {

        }
    }
}
