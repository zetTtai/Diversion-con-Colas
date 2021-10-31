using System;
using System.Net.Sockets;
using System.Text;
using Confluent.Kafka;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Sensores
{
    internal class Sensor
    {
        public static string SensorId {  get; set; }
        private static ProducerConfig ProducerConfig = new ProducerConfig
        {
            BootstrapServers = "",
            SecurityProtocol = SecurityProtocol.SaslPlaintext,
            SaslMechanism = SaslMechanism.ScramSha256,
            SaslUsername = "ickafka",
            SaslPassword = "****"
        };

        public static int Population;

        public static bool EnviarInfo()
        {
            using (var Producer = new ProducerBuilder<Null, string>(Sensor.ProducerConfig).Build())
            {
                try
                {
                    var Result = Producer.ProduceAsync("test", new Message<Null, string> { Value = Sensor.Data() }).Result;
                    Console.WriteLine($"Delivered '{Result.Value}' to: {Result.TopicPartitionOffset}");
                    return true;
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.Message);
                    return false;
                }
            }
        }

        public static void InitializeKafkaServers(string IPKafka, int PortKafka)
        {
            Sensor.ProducerConfig.BootstrapServers = IPKafka + ":" + PortKafka;
        }

        private static void Send(Socket sender, string data)
        { 
            byte[] byteData = Encoding.ASCII.GetBytes(data);
            sender.Send(byteData);
        }

        private static string Data()
        {
            return JsonConvert.SerializeObject(new
            {
                sensor_id = Sensor.SensorId,
                population = Population
            });
        }


    }
}
