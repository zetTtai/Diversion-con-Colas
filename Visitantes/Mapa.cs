using Confluent.Kafka;
using System;
using System.Threading;

namespace Visitantes
{
    internal class Mapa
    {
        public static int MAP_SIZE = 20;
        public int[,] Casillas = new int[MAP_SIZE, MAP_SIZE];
        public static ConsumerConfig KafkaConfig = new ConsumerConfig
        {
            BootstrapServers = "",
            SecurityProtocol = SecurityProtocol.SaslPlaintext,
            SaslMechanism = SaslMechanism.ScramSha256,
            SaslUsername = "ickafka",
            SaslPassword = "****",
            GroupId = "my-group"
        };
        public static Thread thread;

        public Mapa()
        {
            for (int i = 0; i < MAP_SIZE; i++)
            {
                for (int j = 0; j < MAP_SIZE; j++)
                {
                    
                }
            }
        }

        public static void ActualizarMapa()
        {
            using (var consumer = new ConsumerBuilder<Null, string>(Mapa.KafkaConfig).Build())
            {
                consumer.Subscribe("mapa");
                try
                {
                    while (true)
                    {
                        var consumeResult = consumer.Consume();
                        Console.WriteLine(consumeResult.Message.Value);
                        // TODO 
                    }
                }
                catch (Exception)
                {
                    consumer.Close();
                }
            }
        }

    }
}
