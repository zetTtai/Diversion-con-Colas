using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Visitantes
{
    internal class Visitor
    {
        public string Alias;
        public string Name;
        public string Password;

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

        internal bool EnterPark()
        {
            return false;
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

        internal bool Exit()
        {
            throw new NotImplementedException();
        }

        private static string JSONData(Visitor v, string mode)
        {
            return JsonConvert.SerializeObject(new
            {
                action = mode,
                alias = v.Alias,
                name = v.Name,
                pass = v.Password
            });

        }
    }
}
