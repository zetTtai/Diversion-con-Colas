using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Visitantes
{
    internal class Visitante
    {
        public int Id;
        public string Name;
        public string Password;

        public Visitante()
        {
            Name = Faker.Internet.UserName();
            Id = Faker.RandomNumber.Next(0, 999999999);
            Password = Faker.Identification.UkPassportNumber();
        }




    }
}
