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

        private void Conectar_Click(object sender, EventArgs e)
        {
            if(Conectar.Text == "Registrarse")
            {
                Connection.InitializeRegistryServer(IPValueRegistry.Text, (int)PortValueRegistry.Value);
                Program.VisitorOwn = new Visitor();
                if(Program.VisitorOwn.SignIn(VisitorAlias.Text, VisitorName.Text, VisitorPassword.Text))
                {
                    if (Program.VisitorOwn.EnterPark())
                    {
                        Conectar.Text = "Editar";
                        Temporizador.Start();
                    }
                } 
            }
            else
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
        }

        private void Desconectar_Click(object sender, EventArgs e)
        {
            if(Conectar.Text == "Editar")
            {
                if (Program.VisitorOwn.Exit())
                {
                    Conectar.Text = "Registrarse";
                    Temporizador.Stop();
                }
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

        private String HexConverter(Color c)
        {
            return "#" + c.R.ToString("X2") + c.G.ToString("X2") + c.B.ToString("X2");
        }
    }
}
