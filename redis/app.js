const axios = require('axios');
const express = require('express');
const RedisSMQ = require('rsmq');
const bodyParser = require('body-parser');
const fs = require('fs');
const cors = require('cors');
const os = require('os');
//const {exec} = require('child_process');
const Docker = require('dockerode');
const diskusage = require('diskusage');
const osUtils = require('os-utils');
const crypto = require('crypto');
const docker = new Docker();


const app = express();
const port = 3000;
//Conexion para contenedor de  redis
const rsmq = new RedisSMQ({ host: '172.20.0.5', port: 6379 });



  
//app.options('/receive-data', cors());
app.options('*', cors());
app.options('/data_selenium', cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.json());
app.use(cors());


const queueName = 'proyecto';
//son 32 caracteres de encriptacion
const claveEncriptacion = `%=Pma.f.:g%7f4Z+H_8j:w@S)WquS-B,`;


function encryptData(data) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(claveEncriptacion, 'utf-8'), iv);
  const encryptedData = Buffer.concat([cipher.update(JSON.stringify(data), 'utf-8'), cipher.final()]);
  return { iv: iv.toString('hex'), encryptedData: encryptedData.toString('hex') };
}

// Verificar si la cola existe, si no, créala
rsmq.createQueue({ qname: queueName }, (err, resp) => {
  if (err && err.name !== 'queueExists') {
    console.error('Error al crear la cola en RSMQ:', err);
  } else {
    console.log('Cola creada o ya existente en RSMQ');
  }
});

// Ruta para recibir información de Python y procesarla
app.post('/data_selenium', async (req, res) => {
  try {
    const informacion = req.body.data;
    //console.log(informacion);
    const mensajeEncriptado = encryptData(informacion);
    console.log(mensajeEncriptado);
    // Enviar mensaje a la cola
    rsmq.sendMessage({ qname: queueName, message: JSON.stringify(mensajeEncriptado) }, (err, resp) => {
      if (err) {
        console.error('Error al enviar mensaje a RSMQ:', err);
        res.status(500).send('Error interno del servidor');
      } else {
        console.log('Mensaje enviado a RSMQ:', resp);
        res.status(200).json({ success: true });
      }
    });
  } catch (error) {
    console.error('Error en la gestión de la solicitud:', error);
    res.status(500).send('Error interno del servidor');
  }
});



app.post('/data_play', async (req, res) => {
  try {
    const informacion = req.body.data;
    //console.log(informacion);
    const mensajeEncriptado = encryptData(informacion);
    console.log(mensajeEncriptado);
    // Enviar mensaje a la cola
    rsmq.sendMessage({ qname: queueName, message: JSON.stringify(mensajeEncriptado) }, (err, resp) => {
      if (err) {
        console.error('Error al enviar mensaje a RSMQ:', err);
        res.status(500).send('Error interno del servidor');
      } else {
        console.log('Mensaje enviado a RSMQ:', resp);
        res.status(200).json({ success: true });
      }
    });
  } catch (error) {
    console.error('Error en la gestión de la solicitud:', error);
    res.status(500).send('Error interno del servidor');
  }
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

async function generarPDFPlay(datos, informacion) {
  const pdfFileName = 'informe_play.pdf';
  const doc = new PDFDocument();
  const pdfStream = fs.createWriteStream(pdfFileName);

  // Personaliza el contenido del PDF según tus datos y la información adicional
  doc.text('Informe PDF basado en datos de Redis RSMQ y la información de Playwright:', 50, 50);
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



app.post('/docker/selenium',async(req,res)=>{
  const data = req.body;
  var type = data['type']
  if (type == "0"){
    const container = docker.getContainer(data['name']);
    await container.start();
    res.status(200).send('Contenedor iniciado');
  }else if(type == "1"){
    const container = docker.getContainer(data['name']);
    await container.restart();
    res.status(200).send('Contenedor reiniciado');
  }else if(type == "2"){
    const container = docker.getContainer(data['name']);
    await container.stop();
    res.status(200).send('Contenedor detenido');
  }

  
  
});

app.get('/docker',async(_,res)=>{
  const containerNames = ['so1-p1f1_201900822-python_app-1'];
  //const container = docker.getContainer('so1-p1f1_201900822-python_app-1')
  const containerPromises = containerNames.map(async (containerName) => {
    const container = docker.getContainer(containerName);
    return new Promise((resolve, reject) => {
      container.stats({ stream: false }, (err, stats) => {
        if (err) {
          reject(`Error al obtener estadísticas del contenedor ${containerName}: ${err}`);
          return;
        }
        var ramUsage, memLimit, memPercentage,precpuStats,networkIO, cpuPercentage, netIO;
        try {
          ramUsage = stats.memory_stats.usage;
          memLimit = stats.memory_stats.limit;
          memPercentage = ((ramUsage / memLimit) * 100).toFixed(2);
          precpuStats = stats.precpu_stats;
          cpuPercentage = ((stats.cpu_stats.cpu_usage.total_usage - precpuStats.cpu_usage.total_usage) / (stats.cpu_stats.system_cpu_usage - precpuStats.system_cpu_usage) * 100).toFixed(2);
          networkIO = stats.networks.eth0;
          netIO = `${networkIO.rx_bytes} / ${networkIO.tx_bytes}`;
        }catch (error){
          ramUsage = 0;
          memLimit = 0;
          memPercentage = 0;
          cpuPercentage = 0;
          netIO = 0;
        }
        const containerInfo = {
          name: containerName,
          cpuPercentage,
          ramUsage,
          memLimit,
          memPercentage,
          netIO,
        };

        resolve(containerInfo);
      });
    });
  });

  const containerInfos = await Promise.all(containerPromises);

  // Mostrar la información de todos los contenedores
  /*containerInfos.forEach((containerInfo) => {
    console.log(`Información del contenedor ${containerInfo.name}:`);
    console.log(`CPU%: ${containerInfo.cpuPercentage}%`);
    console.log(`RAM: ${containerInfo.ramUsage / (1024 * 1024)}MB / LIMIT ${containerInfo.memLimit / (1024 * 1024 * 1024)}GB`);
    console.log(`MEM%: ${containerInfo.memPercentage}%`);
    console.log(`NET: ${containerInfo.netIO}`);
    console.log();
  });*/
  const result = {
    containers: containerInfos,
    timestamp: new Date().toISOString(),
  };

  res.json(result);

})

app.post('/docker/playwright',async(req,res)=>{
  const data = req.body;
  var type = data['type']
  if (type == "0"){
    const container = docker.getContainer(data['name']);
    await container.start();
    res.status(200).send('Contenedor iniciado');
  }else if(type == "1"){
    const container = docker.getContainer(data['name']);
    await container.restart();
    res.status(200).send('Contenedor reiniciado');
  }else if(type == "2"){
    const container = docker.getContainer(data['name']);
    await container.stop();
    res.status(200).send('Contenedor detenido');
  }



  
  
});

app.get('/docker/playwright',async(_,res)=>{
  const containerNames = ['so1-p1f1_201900822-python_app_2-1'];
  //const container = docker.getContainer('so1-p1f1_201900822-python_app-1')
  const containerPromises = containerNames.map(async (containerName) => {
    const container = docker.getContainer(containerName);
    
    return new Promise((resolve, reject) => {
      container.stats({ stream: false }, (err, stats) => {
        if (err) {
          reject(`Error al obtener estadísticas del contenedor ${containerName}: ${err}`);
          return;
        }
        var ramUsage, memLimit, memPercentage,precpuStats,networkIO, cpuPercentage, netIO;
        try {
          ramUsage = stats.memory_stats.usage;
          memLimit = stats.memory_stats.limit;
          memPercentage = ((ramUsage / memLimit) * 100).toFixed(2);
          precpuStats = stats.precpu_stats;
          cpuPercentage = ((stats.cpu_stats.cpu_usage.total_usage - precpuStats.cpu_usage.total_usage) / (stats.cpu_stats.system_cpu_usage - precpuStats.system_cpu_usage) * 100).toFixed(2);
          networkIO = stats.networks.eth0;
          netIO = `${networkIO.rx_bytes} / ${networkIO.tx_bytes}`;
        }catch (error){
          ramUsage = 0;
          memLimit = 0;
          memPercentage = 0;
          cpuPercentage = 0;
          netIO = 0;
        }
        const containerInfo = {
          name: containerName,
          cpuPercentage,
          ramUsage,
          memLimit,
          memPercentage,
          netIO,
        };

        resolve(containerInfo);
      });
    });
  });

  const containerInfos = await Promise.all(containerPromises);

  // Mostrar la información de todos los contenedores
  /*containerInfos.forEach((containerInfo) => {
    console.log(`Información del contenedor ${containerInfo.name}:`);
    console.log(`CPU%: ${containerInfo.cpuPercentage}%`);
    console.log(`RAM: ${containerInfo.ramUsage / (1024 * 1024)}MB / LIMIT ${containerInfo.memLimit / (1024 * 1024 * 1024)}GB`);
    console.log(`MEM%: ${containerInfo.memPercentage}%`);
    console.log(`NET: ${containerInfo.netIO}`);
    console.log();
  });*/
  const result = {
    containers: containerInfos,
    timestamp: new Date().toISOString(),
  };

  res.json(result);

})


app.post('/docker/redis',async(req,res)=>{
  const data = req.body;
  var type = data['type']
  if (type == "0"){
    const container = docker.getContainer(data['name']);
    await container.start();
    res.status(200).send('Contenedor iniciado');
  }else if(type == "1"){
    const container = docker.getContainer(data['name']);
    await container.restart();
    res.status(200).send('Contenedor reiniciado');
  }else if(type == "2"){
    const container = docker.getContainer(data['name']);
    await container.stop();
    res.status(200).send('Contenedor detenido');
  }



  
  
});

app.get('/docker/redis',async(_,res)=>{
  const containerNames = ['so1-p1f1_201900822-redis-1'];
  //const container = docker.getContainer('so1-p1f1_201900822-python_app-1')
  const containerPromises = containerNames.map(async (containerName) => {
    const container = docker.getContainer(containerName);
    
    return new Promise((resolve, reject) => {
      container.stats({ stream: false }, (err, stats) => {
        if (err) {
          reject(`Error al obtener estadísticas del contenedor ${containerName}: ${err}`);
          return;
        }
        var ramUsage, memLimit, memPercentage,precpuStats,networkIO, cpuPercentage, netIO;
        try {
          ramUsage = stats.memory_stats.usage;
          memLimit = stats.memory_stats.limit;
          memPercentage = ((ramUsage / memLimit) * 100).toFixed(2);
          precpuStats = stats.precpu_stats;
          cpuPercentage = ((stats.cpu_stats.cpu_usage.total_usage - precpuStats.cpu_usage.total_usage) / (stats.cpu_stats.system_cpu_usage - precpuStats.system_cpu_usage) * 100).toFixed(2);
          networkIO = stats.networks.eth0;
          netIO = `${networkIO.rx_bytes} / ${networkIO.tx_bytes}`;
        }catch (error){
          ramUsage = 0;
          memLimit = 0;
          memPercentage = 0;
          cpuPercentage = 0;
          netIO = 0;
        }
        const containerInfo = {
          name: containerName,
          cpuPercentage,
          ramUsage,
          memLimit,
          memPercentage,
          netIO,
        };

        resolve(containerInfo);
      });
    });
  });

  const containerInfos = await Promise.all(containerPromises);

  // Mostrar la información de todos los contenedores
 /*containerInfos.forEach((containerInfo) => {
    console.log(`Información del contenedor ${containerInfo.name}:`);
    console.log(`CPU%: ${containerInfo.cpuPercentage}%`);
    console.log(`RAM: ${containerInfo.ramUsage / (1024 * 1024)}MB / LIMIT ${containerInfo.memLimit / (1024 * 1024 * 1024)}GB`);
    console.log(`MEM%: ${containerInfo.memPercentage}%`);
    console.log(`NET: ${containerInfo.netIO}`);
    console.log();
  });*/
  const result = {
    containers: containerInfos,
    timestamp: new Date().toISOString(),
  };

  res.json(result);

})






app.get('/recursos', async (req, res) => {
  // Obtener información de memoria
  const totalMemory = os.totalmem();
  const freeMemory = os.freemem();
  const usedMemory = totalMemory - freeMemory;

  // Obtener información de disco
  const diskInfo = diskusage.checkSync('/');
  const usedDiskSpace = diskInfo.total - diskInfo.free;

  // Obtener información de uso de CPU
  let cpuUsage = 0;
  await new Promise((resolve) => {
    osUtils.cpuUsage((value) => {
      cpuUsage = value * 100; // Convertir a porcentaje
      resolve();
    });
  });

  // Crear objeto JSON de respuesta
  const responseJSON = {
    memory: {
      total: totalMemory,
      used: usedMemory,
      free: freeMemory
    },
    disk: {
      total: diskInfo.total,
      used: usedDiskSpace,
      free: diskInfo.free
    },
    cpu: {
      usage: cpuUsage
    }
  };

  // Enviar respuesta en formato JSON
  res.status(200).json(responseJSON);
});


app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
}
);
