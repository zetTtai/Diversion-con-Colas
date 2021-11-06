using System;
using System.Drawing;
using System.Windows.Forms;

namespace Visitantes
{
    public partial class Visitante : Form
    {

        public Visitante()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            int PanelSize = Mapa.Width / Map.MAP_SIZE;

            for (int i = 0; i < Map.MAP_SIZE; i++)
            {
                for (int j = 0; j < Map.MAP_SIZE; j++)
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

        /*
         * EVENT HANDLERS
         * 
         */

        private void Registro_Click(object sender, EventArgs e)
        {
            AddMessageToLog("Procediendo a registrar al usuario", 1);
            Connection.InitializeRegistryServer(IPValueRegistry.Text, (int)PortValueRegistry.Value);
            Program.VisitorOwn = new Visitor();
            if(Program.VisitorOwn.SignIn(VisitorAlias.Text, VisitorName.Text, VisitorPassword.Text))
            {
                RegisterStatus(false);
                ParkStatus(true);
            } 

        }

        private void Entrar_Click(object sender, EventArgs e)
        {
            if (Program.VisitorOwn is null)
            {
                Program.VisitorOwn = new Visitor()
                {
                    Alias = VisitorAlias.Text,
                    Name = VisitorName.Text,
                    Password = VisitorPassword.Text,
                };
            }

            AddMessageToLog("Verificando la conexión con Kafka", 1);
            Connection.InitializeKafkaServers(IPValueKafka.Text, (int)PortValueKafka.Value);
            if (Connection.CheckServerAvaliability())
            {
                AddMessageToLog("Se ha podido conectar con Kafka", 2);
            }
            else
            {
                AddMessageToLog("No se ha podido conectar con Kafka", 0);
                return;
            }

            AddMessageToLog("Intentando entrar al parque...", 1);
            if (Program.VisitorOwn.EnterPark())
            {
                VisitorStatus(false);
                ParkStatus(true);
            }
        }

        private void Editar_Click(object sender, EventArgs e)
        {
            if (Program.VisitorOwn.EditInfo(VisitorAlias.Text, VisitorName.Text, VisitorPassword.Text))
            {

            }
            else
            {
                VisitorAlias.Text = Program.VisitorOwn.Alias;
                VisitorName.Text = Program.VisitorOwn.Name;
                VisitorPassword.Text = Program.VisitorOwn.Password;
            }
        }

        private void Salir_Click(object sender, EventArgs e)
        {
            AddMessageToLog("Intentando salir del parque...", 1);
            if(Program.VisitorOwn.Exit())
            {
                VisitorStatus(true);
                ParkStatus(false);
            }
        }

        private void Temporizador_Tick(object sender, EventArgs e)
        {

        }

        private void Alias_Enter(object sender, EventArgs e)
        {
            if(ColorPicker.ShowDialog() == DialogResult.OK)
            {
                VisitorAlias.Text = HexConverter(ColorPicker.Color);
            }
        }

        /*
         * AUXILIAR METHODS
         */
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
            else // WARNING
            {
                aux.ForeColor = Color.FromArgb(255, 193, 7);
            }

            this.Logs.Controls.Add(aux);
            this.Logs.VerticalScroll.Value = this.Logs.VerticalScroll.Maximum;
        }

        private void RegisterStatus(bool status)
        {
            IPValueRegistry.Enabled = status;
            PortValueRegistry.Enabled = status;
        }

        private void VisitorStatus(bool status)
        {
            VisitorAlias.Enabled = status;
            VisitorName.Enabled = status;
            VisitorPassword.Enabled = status;
        }

        private void ParkStatus(bool status)
        {
            Entrar.Enabled = status;
            Salir.Enabled = !status;
        }

        private String HexConverter(Color c)
        {
            return "#" + c.R.ToString("X2") + c.G.ToString("X2") + c.B.ToString("X2");
        }

    }
}
