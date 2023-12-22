const path = require("path");
const express = require("express");
const WebSocket = require("ws");
const app = express();
const fs = require('fs');

const WS_PORT = 8888;
const HTTP_PORT = 8000;

const wsServer = new WebSocket.Server({ port: WS_PORT }, () => {console.log("WebSocket server is running on port " + WS_PORT)});

let connectedClients = [];
wsServer.on("connection", (ws, req) => {
	console.log("Terhubung");
	ws.on("message", (data) => {
		if (data.indexOf("WEB_CLIENT") !== -1) {
			connectedClients.push(ws);
			console.log("WEB TER-AKSES");
			return;
		}
		// Remove disconnected clients
        connectedClients = connectedClients.filter(client => client.readyState === WebSocket.OPEN);

        // Send data to connected clients
        connectedClients.forEach(client => {
            client.send(data, (error) => {
                if (error) {
                    console.error("Error sending data to client: ", error);
                }
            });
        });
	});

	ws.on("close", () => {
        console.log("Connection closed");
        connectedClients = connectedClients.filter(client => client !== ws);
    });

	ws.on("error", (error) => {
		console.error("WebSocket error observed: ", error);
	});
});

app.get("/stress_level", (req, res) => {
    console.log("Request received for /stress_level");
    // Membaca file JSON yang ditulis oleh script Python
    fs.readFile('./most_common_stress_level.json', 'utf8', (err, data) => {
        if (err) {
            console.error("Error reading most_common_stress_level.json:", err);
            return res.status(500).json({ error: "Internal Server Error" });
        }
        const jsonData = JSON.parse(data);
        console.log("Data fetched:", jsonData);
        res.json(jsonData);
    });
});

app.use(express.static("."));
app.get("/user", (req, res) => res.sendFile(path.resolve(__dirname, "./user.html")));
app.listen(HTTP_PORT, () => {
    console.log("HTTP server is running on port " + HTTP_PORT);
});