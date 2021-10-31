using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Visitantes
{
    internal class Atracciones
    {
        public int Id;
        public int TiempoEspera;
        public Tuple<int, int> Coords;

        public Atracciones(int id, int x, int y)
        {
            Id = id;
            Coords = new Tuple<int, int>(x, y);
        }

    }
}
