using Confluent.Kafka;
using Newtonsoft.Json.Linq;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Visitantes
{
    internal class Conection
    {
        private static IPAddress IPRegistry;
        private static int PortRegistry;

        private static ConsumerConfig ConsumerConfig = new ConsumerConfig
        {
            BootstrapServers = "",
            SecurityProtocol = SecurityProtocol.SaslPlaintext,
            SaslMechanism = SaslMechanism.ScramSha256,
            SaslUsername = "ickafka",
            SaslPassword = "****",
            GroupId = "mapa"
        };

        private static ProducerConfig ProducerConfig = new ProducerConfig
        {
            BootstrapServers = "",
            SecurityProtocol = SecurityProtocol.SaslPlaintext,
            SaslMechanism = SaslMechanism.ScramSha256,
            SaslUsername = "ickafka",
            SaslPassword = "****"
        };

        public static void InitializeKafkaServers(string IPKafka, int PortKafka)
        {
            Conection.ProducerConfig.BootstrapServers = IPKafka + ":" + PortKafka;
            Conection.ConsumerConfig.BootstrapServers = IPKafka + ":" + PortKafka;
        }

        public static void InitializeRegistryServer(string IPRegistry, int PortRegistry)
        {
            Conection.IPRegistry = IPAddress.Parse(IPRegistry);
            Conection.PortRegistry = PortRegistry;
        }

        public static bool RegistryCommunication(string Data)
        {
            if (Conection.IPRegistry != null && Conection.IPRegistry.ToString() != "")
            {
                try
                {
                    IPEndPoint ipe = new IPEndPoint(Conection.IPRegistry, Conection.PortRegistry);
                    Socket ConnectionSocket = new Socket(ipe.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
                    ConnectionSocket.ReceiveTimeout = 5000;
                    byte[] BufferSend = Encoding.ASCII.GetBytes(Data);
                    byte[] BufferReceive = new byte[2048];

                    ConnectionSocket.Connect(ipe);
                    ConnectionSocket.Send(BufferSend);
                    ConnectionSocket.Receive(BufferReceive);
                    ConnectionSocket.Shutdown(SocketShutdown.Both);
                    ConnectionSocket.Close();

                    JObject json = JObject.Parse(BufferReceive.ToString());

                    if (json.ContainsKey("status") && json.Value<int>("status") == 0)
                    {
                        return true;
                    }
                    else
                    {
                        Console.WriteLine(json.ToString());
                        return false;
                    }
                        
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.ToString());
                    return false;
                }
            }
            else
            {
                Console.WriteLine("IP for Kafka is null or not an IP");
                return false;
            }
        }

        public static void Consume(string Topic = "mapa")
        {
            using (var Consumer = new ConsumerBuilder<Null, string>(Conection.ProducerConfig).Build())
            {
                Consumer.Subscribe(Topic);
                try
                {
                    while (true)
                    {
                        var ConsumeResult = Consumer.Consume();
                        Console.WriteLine(ConsumeResult.Message.Value);
                        // TODO 
                    }
                }
                catch (Exception e)
                {
                    Consumer.Close();
                    throw e;
                }
            }
        }

        public static void Produce(string Message, string Topic = "visitantes")
        {
            using (var Producer = new ProducerBuilder<Null, string>(Conection.ProducerConfig).Build())
            {
                try
                {
                    var Result = Producer.ProduceAsync("test", new Message<Null, string> { Value = Message }).Result;
                    Console.WriteLine($"Delivered '{Result.Value}' to: {Result.TopicPartitionOffset}");
                }
                catch (Exception e)
                {
                    throw e;
                }
            }
        }



    }
}
