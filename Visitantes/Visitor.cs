using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Visitantes
{
    internal class Visitor
    {
        public string Alias;
        public string Name;
        public string Password;
        public Tuple<int, int> Coords;

        public static Task ConsumeVisitantes;
        public static bool ReadingVisitantes;
        public static Task ConsumeMapa;
        public static bool ReadingMapa;

        public Visitor()
        {
            Name = Faker.Name.First();
            Alias = Faker.Internet.UserName(); // TODO: Change to color
            Password = Faker.Identification.UkPassportNumber();
        }

        internal bool SignIn(string alias, string name, string pass)
        {
            string old_alias = Alias; 
            string old_name = Name;
            string old_pass = Password;

            Alias = alias;
            Name = name;
            Password = pass;

            if (Connection.RegistryCommunication(JSONData(this, "create")))
            {
                return true;
            } 
            else
            {
                Alias = old_alias;
                Name = old_name;
                Password = old_pass;
                return false;
            }
        }

        internal bool EditInfo(string alias, string name, string pass)
        {
            string old_alias = Alias;
            string old_name = Name;
            string old_pass = Password;

            Alias = alias;
            Name = name;
            Password = pass;

            if (Connection.RegistryCommunication(JSONData(this, "edit")))
            {
                return true;
            }
            else
            {
                Alias = old_alias;
                Name = old_name;
                Password = old_pass;
                return false;
            }
        }


        internal bool TryEnterPark()
        {
            if(!ReadingVisitantes)
            {
                ReadingVisitantes = true;
                ConsumeVisitantes = Task.Run(() => Connection.Consume("visitantes"));
            }
            return Connection.Produce(JSONData(this, "Entrar"));
        }

        internal static void StopConsumingVisitantes()
        {
            if(ReadingVisitantes)
            {
                ReadingVisitantes = false;
            }
        }


        internal bool Exit()
        {
            bool b = Connection.Produce(JSONData(this, "Salir"));
            Visitor.StopConsumingVisitantes();
            Visitor.StopReadingMapa();
            return b;
        }

        private static string JSONData(Visitor v, string mode)
        {
            return JsonConvert.SerializeObject(new
            {
                action = mode,
                id = v.Alias,
                name = v.Name,
                password = v.Password
            });

        }

        private static string JSONMovement(Visitor v, Tuple<int,int> coords)
        {
            return JsonConvert.SerializeObject(new
            {
                X = coords.Item1,
                Y = coords.Item2,
                id = v.Alias,
                name = v.Name,
                password = v.Password
            });

        }

        internal Tuple<int, int> DecideMovement(List<Attraction> attractions)
        {
            if(attractions == null || attractions.Count == 0)
            {
                throw new ArgumentNullException();
            }

            attractions.Sort();

            int dx = 0, dy = 0;
            for(int i = 0; dx == dy && dx == 0; i++)
            {
                Attraction objective = attractions[i];
                dx = objective.Coords.Item1 - Program.VisitorOwn.Coords.Item1;
                dy = objective.Coords.Item2 - Program.VisitorOwn.Coords.Item2;
            }

            int cx = 0, cy = 0;
            if (dx < 0 && Math.Abs(dy) < (Map.MAP_SIZE - Math.Abs(dy)))
            {
                cx = -1;
            }
            else if(dx > 0)
            {
                cx = 1;
            }
            
            if (dy > 0 && Math.Abs(dy) < (Map.MAP_SIZE - Math.Abs(dy)))
            {
                cy = 1;
            }
            else if(dy < 0)
            {
                cx = -1;
            }
            
            return new Tuple<int, int>(cx, cy);

        }

        internal bool Move(Tuple<int, int> movimiento)
        {
            return Connection.Produce(JSONMovement(this, movimiento));
        }

        internal static void GetMap()
        {
            if (!ReadingMapa)
            {
                ReadingMapa = true;
                ConsumeMapa = Task.Run(() => Connection.Consume("mapa"));
            }
        }

        internal static void StopReadingMapa()
        {
            if (ReadingMapa)
            {
                ReadingMapa = false;
            }
        }
    }
}
