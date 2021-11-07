using Confluent.Kafka;
using Newtonsoft.Json.Linq;
using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Visitantes
{
    internal class Connection
    {
        private static IPAddress IPRegistry;
        private static int PortRegistry;

        private static ConsumerConfig ConsumerConfig = new ConsumerConfig
        {
            BootstrapServers = "",
            SecurityProtocol = SecurityProtocol.Plaintext,
            SaslMechanism = SaslMechanism.ScramSha256,
            SaslUsername = "",
            SaslPassword = "",
            GroupId = "visitantes",
        };

        private static ProducerConfig ProducerConfig = new ProducerConfig
        {
            BootstrapServers = "",
            SecurityProtocol = SecurityProtocol.Plaintext,
            SaslMechanism = SaslMechanism.ScramSha256,
            SaslUsername = "",
            SaslPassword = "",
            Acks = Acks.Leader
        };

        public static void InitializeKafkaServers(string IPKafka, int PortKafka)
        {
            Connection.ProducerConfig.BootstrapServers = IPKafka + ":" + PortKafka;
            Connection.ConsumerConfig.BootstrapServers = IPKafka + ":" + PortKafka;
        }

        public static void InitializeRegistryServer(string IPRegistry, int PortRegistry)
        {
            Connection.IPRegistry = IPAddress.Parse(IPRegistry);
            Connection.PortRegistry = PortRegistry;
        }

        public static bool RegistryCommunication(string Data)
        {
            if (Connection.IPRegistry != null && Connection.IPRegistry.ToString() != "")
            {
                try
                {
                    Program.UI.Invoke(Program.UI.AddMessageFunction, "Se ha enviado la siguiente petición a Registry: " + Data, 1);
                    IPEndPoint ipe = new IPEndPoint(Connection.IPRegistry, Connection.PortRegistry);
                    Socket ConnectionSocket = new Socket(ipe.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
                    ConnectionSocket.ReceiveTimeout = 5000;
                    byte[] BufferSend = Encoding.ASCII.GetBytes(Data);
                    byte[] BufferReceive = new byte[2048];

                    ConnectionSocket.Connect(ipe);
                    ConnectionSocket.Send(BufferSend);
                    ConnectionSocket.Receive(BufferReceive);
                    ConnectionSocket.Shutdown(SocketShutdown.Both);
                    ConnectionSocket.Close();

                    JObject json = JObject.Parse(Encoding.Default.GetString(BufferReceive));

                    if (json.ContainsKey("status") && json.Value<int>("status") == 0)
                    {
                        Program.UI.Invoke(Program.UI.AddMessageFunction, "Petición satisfecha correctamente", 2);
                        return true;
                    }
                    else
                    {
                        Program.UI.Invoke(Program.UI.AddMessageFunction, "Se produjo un error creando o modificando el perfil: \n" + json.ToString(), 0);
                        return false;
                    }
                        
                }
                catch (Exception e)
                {
                    Program.UI.Invoke(Program.UI.AddMessageFunction, "Se ha producido un error comunicando con Registry: " + e.Message, 0);
                    return false;
                }
            }
            else
            {
                Program.UI.Invoke(Program.UI.AddMessageFunction, "La IP " + Connection.IPRegistry.ToString() + "es inválida", 0);
                return false;
            }
        }

        public static bool CheckServerAvaliability()
        {
            Program.UI.Invoke(Program.UI.AddMessageFunction, "Comprobando si Kafka esta disponible...", 1);
            var adminConfig = new AdminClientConfig()
            {
                BootstrapServers = ProducerConfig.BootstrapServers
            };

            using (var adminClient = new AdminClientBuilder(adminConfig).Build())
            {
                var metadata = adminClient.GetMetadata(TimeSpan.FromSeconds(3));
                var topicsMetadata = metadata.Topics;
                var topicNames = metadata.Topics.Select(a => a.Topic).ToList();
                return (topicNames.Count > 0);
            }
        }

        public static void Consume(string Topic = "mapa")
        {
            using (var Consumer = new ConsumerBuilder<Null, string>(Connection.ConsumerConfig).Build())
            {
                Consumer.Subscribe(Topic);
                try
                {
                    while (true)
                    {
                        if((Topic == "visitantes" && Visitor.ReadingVisitantes) || (Topic == "mapa" && Visitor.ReadingMapa))
                        {
                            var ConsumeResult = Consumer.Consume();
                            JObject json = JObject.Parse(ConsumeResult.Message.Value);
                            Program.UI.Invoke(Program.UI.AddMessageFunction, json.ToString(), 1);
                            if (ConsumeResult != null && ConsumeResult.Topic == "visitantes" && json.ContainsKey("status") && json["id"].ToString() == Program.VisitorOwn.Alias)
                            {
                                if (ConsumeResult.Message.Timestamp.UnixTimestampMs >= Program.TimeStamp)
                                {
                                    Program.UI.Invoke(Program.UI.AddMessageFunction, json.ToString(), 1);
                                    Program.UI.Invoke(Program.UI.EngineResponseFunction, json);
                                }
                            }
                            else if (ConsumeResult != null && ConsumeResult.Topic == "mapa")
                            {
                                if (ConsumeResult.Message.Timestamp.UnixTimestampMs >= Program.TimeStamp)
                                {
                                    Program.UI.Invoke(Program.UI.AddMessageFunction, "Mapa:" + json.ToString(), 1);
                                    Program.UI.Invoke(Program.UI.EngineResponseFunction, json);
                                }
                            }
                        } 
                        else
                        {
                            Program.UI.Invoke(Program.UI.AddMessageFunction, "Eh? Que hago aqui? T:" + Topic + ", Map:" + Visitor.ReadingMapa + ", V:" + Visitor.ReadingVisitantes, 0);
                            break;
                        }
                    }
                }
                catch (Exception e)
                {
                    Consumer.Close();
                    Program.UI.Invoke(Program.UI.AddMessageFunction, "Se ha producido un error mientras se consumía un mensaje para el topic " + Topic, 0);
                    throw e;
                }
            }
        }

        public static bool Produce(string Message, string Topic = "visitantes")
        {
            using (var Producer = new ProducerBuilder<Null, string>(Connection.ProducerConfig).Build())
            {
                try
                {
                    Producer.ProduceAsync(Topic, new Message<Null, string> { Value = Message }).Wait();
                    Program.UI.Invoke(Program.UI.AddMessageFunction, "Se ha enviado " + Message, 2);
                    return true;
                }
                catch (Exception e)
                {
                    Program.UI.Invoke(Program.UI.AddMessageFunction, "Se ha producido un error mientras se producía un mensaje para el topic " + Topic, 0);
                    return false;
                }
            }
        }
    }
}
