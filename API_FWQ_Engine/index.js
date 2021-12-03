const path = require('path')
var express = require('express')

var app = express()
app.use(express.json())

//----------------------------------------------------------------------------------------------------------------
// DATABASE
//----------------------------------------------------------------------------------------------------------------

const knex = require('knex')({ 
    client: "sqlite3",
    connection: {
        filename: path.resolve(__dirname, "../db/database.db")
    },
    useNullAsDefault: true
})

//----------------------------------------------------------------------------------------------------------------
// Funciones
//----------------------------------------------------------------------------------------------------------------

async function show(table, idUser) {
   obj = {}
   if(idUser == 0) {
      var datos = await knex.select().table(table)
      var cuenta = await knex.select().table(table).count('* as total')
      obj.total = cuenta[0].total
      obj.datos = datos
   }
   else {
      var datos = await knex(table).where('id_owner', idUser)
      var cuenta = await knex(table).where('id_owner', idUser).count('* as total')
      obj.total = cuenta[0].total
      obj.datos = datos
   }
   return obj
}

//----------------------------------------------------------------------------------------------------------------
// Peticiones
//----------------------------------------------------------------------------------------------------------------

app.get('/fwq/visitors', async function(pet, resp) { 
   try {
      obj = await show('visitantes', 0)
      resp.status(200).send(obj)
   }
   catch(error) {
      console.log(error)
      resp.status(500).send({error:error})
   }
})

app.get('/fwq/attractions', async function(pet, resp) { 
   try {
      obj = await show('atracciones', 0)
      resp.status(200).send(obj)
   }
   catch(error) {
      console.log(error)
      resp.status(500).send({error:error})
   }
})

app.get('/fwq/logs', async function(pet, resp) { 
   try {
      obj = await show('registros', 0)
      resp.status(200).send(obj)
   }
   catch(error) {
      console.log(error)
      resp.status(500).send({error:error})
   }
})


app.get('/fwq/map', async function(pet, resp) {
   try {
      obj = {}
      attractions = await show('atracciones', 0)
      visitors = await show('visitantes', 0)
      obj = {
         "atracciones" : attractions["datos"],
         "visitantes" : visitors["datos"]
      }
      resp.status(200).send(obj)
   }
   catch(err) {
      console.log(error)
      resp.status(500).send({error:error})
   }
});

var listener = app.listen(process.env.PORT||3000, () => {
   console.log(`Servidor en el puerto ${listener.address().port}`);
});