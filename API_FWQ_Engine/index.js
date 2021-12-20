const path = require('path')
const fs = require('fs') // Para leer documentos
var express = require('express')
const https = require('https')
const port = 3001

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


app.get('/fwq/map', function(pet, resp) {
   try {
      var rawdata = fs.readFileSync("../mapa.json");
      var mapa = JSON.parse(rawdata);
      resp.status(200).send(mapa);
   }
   catch(error) {
      resp.status(404).send({error:"No hay un mapa generado"});
   }
});

/*
var listener = app.listen(process.env.PORT||3000, () => {
   console.log(`Servidor en el puerto ${listener.address().port}`);
});*/

const httpsOptions = {
   key: fs.readFileSync('./key.pem'),
   cert: fs.readFileSync('./cert.pem')
}

const server = https.createServer(httpsOptions, app).listen(port, "127.0.0.1", () => {
   console.log('server running at ' + port)
});