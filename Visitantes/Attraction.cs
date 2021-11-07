using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Visitantes
{
    internal class Attraction : IComparable<Attraction>
    {
        public string Id;
        public double TiempoEspera;
        public Tuple<int, int> Coords;

        public int CompareTo(Attraction other)
        {
            if (this.TiempoEspera == other.TiempoEspera)
                return 0;
            return this.TiempoEspera < other.TiempoEspera ? -1 : 1;
        }
    }
}
