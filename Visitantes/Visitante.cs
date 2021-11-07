using Newtonsoft.Json.Linq;
using System;
using System.Drawing;
using System.Globalization;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Visitantes
{
    public partial class Visitante : Form
    {
        public delegate void AddMessage(string message, int mode);
        public delegate void EngineMessage(JObject json);
        public AddMessage AddMessageFunction;
        public EngineMessage EngineResponseFunction;
        private bool _wannaExit = false;
        private bool _wannaEnter = false;

        public Visitante()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            AddMessageFunction = new AddMessage(AddMessageToLog);
            EngineResponseFunction = new EngineMessage(EngineResponse);
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
                        Name = i + "," + j,
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
            if (Program.VisitorOwn is null)
            {
                Program.VisitorOwn = new Visitor
                {
                    Alias = VisitorAlias.Text,
                    Name = VisitorName.Text,
                    Password = VisitorPassword.Text
                };
            }
            if(Program.VisitorOwn.SignIn(VisitorAlias.Text, VisitorName.Text, VisitorPassword.Text))
            {
                RegisterStatus(false);
                ParkStatus(true);
            } 

        }
        private void Editar_Click(object sender, EventArgs e)
        {
            if (Program.VisitorOwn is null)
            {
                Program.VisitorOwn = new Visitor
                {
                    Alias = VisitorAlias.Text,
                    Name = VisitorName.Text,
                    Password = VisitorPassword.Text
                };
            }
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

        private void Entrar_Click(object sender, EventArgs e)
        {
            _wannaEnter = true;
            if (Program.VisitorOwn is null)
            {
                Program.VisitorOwn = new Visitor()
                {
                    Alias = VisitorAlias.Text,
                    Name = VisitorName.Text,
                    Password = VisitorPassword.Text,
                };
            }

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
            if (Program.VisitorOwn.TryEnterPark())
            {
                VisitorStatus(false);
            }
        }

        private void Salir_Click(object sender, EventArgs e)
        {
            _wannaExit = true;
            AddMessageToLog("Intentando salir del parque...", 1);
            if(Program.VisitorOwn != null && Program.VisitorOwn.Exit())
            {
                VisitorStatus(true);
            }
        }

        private void EngineResponse(JObject json)
        {
            if (_wannaEnter && json.ContainsKey("status"))
            {
                if(json["status"].ToString() == "0" || json["status"].ToString() == "3")
                {
                    Program.UI.Invoke(AddMessageFunction, "Se ha entrado al parque correctamente", 2);
                    _wannaEnter = false;
                    ParkStatus(false);
                    Visitor.GetMap();
                }
                else
                {
                    Program.UI.Invoke(AddMessageFunction, "Se ha rechazado la petición de entrada: " + json, 0);
                    ParkStatus(true);
                }   
            }
            else if (_wannaExit && json.ContainsKey("status"))
            {
                if (json["status"].ToString() == "0")
                {
                    Program.UI.Invoke(AddMessageFunction, "Se ha salido del parque correctamente", 2);
                    _wannaExit = false;
                    Visitor.StopConsumingVisitantes();
                    Temporizador.Enabled = false;
                    ParkStatus(true);
                }
                else
                {
                    Program.UI.Invoke(AddMessageFunction, "Se ha rechazado la petición de salida: " + json, 0);
                    ParkStatus(false);
                }
            }
            else if(json.ContainsKey("atracciones"))
            {
                Temporizador.Enabled = true;
                Program.UI.Invoke(AddMessageFunction, "Mapa: " + json, 2);
                Program.Attractions.Clear();
                foreach (var item in json["atracciones"])
                {
                    Program.Attractions.Add(new Attraction
                    {
                        Id = item["id"].ToString(),
                        TiempoEspera = int.Parse(item["tiempo"].ToString()),
                        Coords = new Tuple<int, int>(int.Parse(item["X"].ToString()), int.Parse(item["Y"].ToString()))
                    });
                }
                Program.Visitors.Clear();
                foreach (var item in json["visitantes"])
                {
                    Program.Visitors.Add(new Visitor {
                        Alias = item["id"].ToString(),
                        Coords = new Tuple<int, int>(int.Parse(item["X"].ToString()), int.Parse(item["Y"].ToString()))
                    });
                }
                ActualizarMapa();
            }
        }

        private void ActualizarMapa()
        {
            foreach(Panel p in Mapa.Controls)
            {
                p.BackColor = Color.Transparent;
                p.Controls.Clear();
            }

            foreach (Visitor v in Program.Visitors)
            {
                ((Panel)Mapa.Controls.Find(v.Coords.Item1 + "," + v.Coords.Item2, false)[0]).BackColor = ColorConverter(v.Alias);

                if(v.Alias == Program.VisitorOwn.Alias)
                {
                    Program.VisitorOwn.Coords = v.Coords;
                }

            }

            foreach (Attraction a in Program.Attractions)
            {
                Label l = new Label
                {
                    Text = a.Id.ToString().ToCharArray()[0].ToString() + a.Id.ToString().ToCharArray()[a.Id.Length - 1].ToString(),
                    Dock = DockStyle.Fill,
                    TextAlign = ContentAlignment.MiddleCenter,
                    ForeColor = Color.White
                };
                ((Panel)Mapa.Controls.Find(a.Coords.Item1 + "," + a.Coords.Item2, false)[0]).Controls.Add(l);
            }
        }

        private void Temporizador_Tick(object sender, EventArgs e)
        {
            Tuple<int,int> movimiento = Program.VisitorOwn.DecideMovement(Program.Attractions);
            AddMessageToLog("Intentando moverse en la dirección: " + movimiento.ToString(), 1);
            if (!Program.VisitorOwn.Move(movimiento))
            {
                AddMessageToLog("Se ha producido un error comunicando el movimiento", 0);
            }
        }


        /*
         * AUXILIAR METHODS
         */
        private void Alias_Enter(object sender, EventArgs e)
        {
            if (ColorPicker.ShowDialog() == DialogResult.OK)
            {
                VisitorAlias.Text = HexConverter(ColorPicker.Color);
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
            Registro.Enabled = status;
            Editar.Enabled = status;
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

        private Color ColorConverter(string colorHex)
        {
            int argb = Int32.Parse(colorHex.Replace("#", "FF"), NumberStyles.HexNumber);
            return Color.FromArgb(argb);
        }

        private void Visitante_FormClosing(object sender, FormClosingEventArgs e)
        {
            Salir_Click(sender, e);
        }
    }
}
