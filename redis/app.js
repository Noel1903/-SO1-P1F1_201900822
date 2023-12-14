// Aplicación Node.js (app.js)
const express = require('express');
const bodyParser = require('body-parser');
const RedisSMQ = require('rsmq');
const cors = require('cors');
const app = express();
const port = 6000;

// Configuración de Redis RSMQ
const rsmq = new RedisSMQ({ host: '172.17.0.2', port: 6379 });
//list_data = []
// Middleware para parsear el cuerpo de las solicitudes como JSON
const corsOptions = {
    origin: 'http://localhost:5000',
    methods: 'POST',
  };
  
  app.use(cors(corsOptions));
  
//app.options('/receive-data', cors());
app.options('*', cors());
app.options('/data', cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.json());
app.use(cors());

// Ruta para recibir información de Python y procesarla
app.post('/data', (req, res) => {
  const informacion = req.body.data;

  // Realizar acciones adicionales con la información recibida
  console.log('Información recibida:', informacion);

  res.status(200).send('Información recibida correctamente');
});

app.get('/',(_,res)=>{
    res.status(200).send('Hola mundo');
    
})

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor Node.js escuchando en http://localhost:${port}`);
});
