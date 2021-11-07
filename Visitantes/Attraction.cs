using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Visitantes
{
    internal class Attraction : IComparable<Attraction>
    {
        public int Id;
        public int TiempoEspera;
        public Tuple<int, int> Coords;

        public Attraction(int id, int x, int y)
        {
            Id = id;
            Coords = new Tuple<int, int>(x, y);
        }

        public int CompareTo(Attraction other)
        {
            if (this.TiempoEspera == other.TiempoEspera)
                return 0;
            return this.TiempoEspera < other.TiempoEspera ? -1 : 1;
        }
    }
}
