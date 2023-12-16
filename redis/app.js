// Aplicación Node.js (app.js)
const express = require('express');
const bodyParser = require('body-parser');
const RedisSMQ = require('rsmq');
const PDFDocument = require('pdfkit');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 6000;
/*const nombreContenedor = "so1-p1f1_201900822-nodejs_app-1"
const pdf_selenium = "/app/informe_selenium.pdf"
// Configuración de Redis RSMQ

// Comando para obtener el contenido de los archivos
const comando = `sudo docker cp ${nombreContenedor}: ${pdf_selenium} /reports`;*/
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
app.options('/data_selenium', cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.json());
app.use(cors());

// Ruta para recibir información de Python y procesarla
app.post('/data_selenium', async (req, res) => {
  const informacion = req.body.data;
  //informacion = JSON.stringify(informacion);
  // Realizar acciones adicionales con la información recibida
  console.log('Información recibida:', informacion);
  //console.log("Obteniendo información en rmsq")
  // Recupera información de Redis RSMQ (ejemplo de datos)
  const datosRedis = ['Dato 1', 'Dato 2', 'Dato 3'];

  // Genera el informe PDF con los datos de Redis RSMQ y la información adicional
  const pdfFileName = await generarPDF([], informacion);

  res.status(200).send('Información recibida correctamente');
});

app.get('/',(_,res)=>{
    res.status(200).send('Hola mundo');
    
})




async function generarPDF(datos, informacion) {
  const pdfFileName = 'informe_selenium.pdf';
  const doc = new PDFDocument();
  const pdfStream = fs.createWriteStream(pdfFileName);

  // Personaliza el contenido del PDF según tus datos y la información adicional
  doc.text('Informe PDF basado en datos de Redis RSMQ y la información de Selenium:', 50, 50);
  doc.text(`Información adicional: ${informacion}`, 50, 70);

  datos.forEach((linea, indice) => {
    doc.text(`${indice + 1}. ${linea}`, 50, 100 + indice * 20);
  });

  // Cierra el flujo de escritura antes de devolver el nombre del archivo
  doc.pipe(pdfStream);
  doc.end();

  await new Promise(resolve => pdfStream.on('finish', resolve));

  console.log(`Informe PDF generado: ${pdfFileName}`);
  return pdfFileName;
}






// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor Node.js escuchando en http://localhost:${port}`);
});
