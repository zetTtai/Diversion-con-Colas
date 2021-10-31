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
            Name = Faker.Internet.UserName();
            //Alias = Faker.RandomNumber.Next(0, 999999999);
            Password = Faker.Identification.UkPassportNumber();
        }

        internal bool SignIn(string text1, string text2, string text3)
        {
            throw new NotImplementedException();
        }

        internal bool EditInfo(string text1, string text2, string text3)
        {
            throw new NotImplementedException();
        }
    }
}
