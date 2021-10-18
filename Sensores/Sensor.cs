using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Sensores
{
    internal class Sensor
    {
        public static string SensorId {  get; set; }

        private static IPAddress Server = IPAddress.Parse("127.0.0.1");
        private static int Port = 9092;

        public static int Population;

        public static bool EnviarInfo()
        {
            try
            {
                IPEndPoint ipe = new IPEndPoint(Server, Port);
                Socket sender = new Socket(ipe.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

                sender.Connect(ipe);
                Send(sender, Data());
                sender.Shutdown(SocketShutdown.Both);
                sender.Close();
                return true;
            }
            catch (System.Exception)
            {
                return false;
            }
        }

        public static void ChangeServer(string newAdress)
        {
            Server = IPAddress.Parse(newAdress);
        }

        public static void ChangePort(int newPort)
        {
            Port = newPort;
        }

        private static void Send(Socket sender, string data)
        { 
            byte[] byteData = Encoding.ASCII.GetBytes(data);
            sender.Send(byteData);
        }

        private static string Data()
        {
            return "{ \"id\" : \"" + SensorId + "\", \"population\" : " + Population + " }";
        }

        public static void ProbarConexion()
        {
            try
            {
                IPEndPoint ipe = new IPEndPoint(Server, Port);
                Socket sender = new Socket(ipe.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

                sender.Connect(ipe);
                sender.Shutdown(SocketShutdown.Both);
                sender.Close();
            }
            catch (System.Exception e)
            {
                throw e;
            }
        }


    }
}
