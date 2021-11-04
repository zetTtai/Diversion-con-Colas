using System;
using Confluent.Kafka;
using Newtonsoft.Json;

namespace Sensores
{
    public class Sensor
    {
        public static string SensorId {  get; set; }
        private static ProducerConfig ProducerConfig = new ProducerConfig
        {
            BootstrapServers = "",
            SecurityProtocol = SecurityProtocol.Plaintext,
            SaslMechanism = SaslMechanism.ScramSha256,
            SaslUsername = "",
            SaslPassword = ""
        };

        public static int Population;

        public static bool EnviarInfo()
        {
            using (var Producer = new ProducerBuilder<Null, string>(Sensor.ProducerConfig).Build())
            {
                try
                {
                    Producer.Produce("sensor", new Message<Null, string> { Value = Sensor.Data() });
                    Program.UI.AddMessageToLog("Se ha publicado en el topic sensor la información " + Sensor.Data(), 2);
                    return true;
                }
                catch (Exception e)
                {
                    Program.UI.AddMessageToLog("Se ha producido un error: " + e.Message, 0);
                    return false;
                }
            }
        }

        public static void InitializeKafkaServers(string IPKafka, int PortKafka)
        {
            
            Sensor.ProducerConfig.BootstrapServers = IPKafka + ":" + PortKafka;
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
