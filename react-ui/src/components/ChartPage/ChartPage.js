import React, {Component} from 'react';
import './ChartPage.css';
import Grid from '@material-ui/core/Grid';
import Container from "@material-ui/core/Container";
import WebSocketWrapper from "../WebSocketWrapper/WebSocketWrapper";

class ChartPage extends Component {
    constructor(props) {
        super(props);
        this.SERVER_URL = "ws://localhost:43968/example_ws/echo-example";
        this.state = {
            data: {},
            network: {},
        }
    }

    handleData = (data) => {
        console.log("Data received");
        data = JSON.parse(data);
        console.log(data);
        this.setState({data: data['ui'], network: data['network']});
    };

    processData = (data) => {
        let rows = [];
        for (let [key, value] of Object.entries(data)) {
            rows.push(this.createRow(key, value["icon"], [value["mouse_usage"], value["keyboard_usage"], value["idle"], value["open"]]));
        }
        return rows;
    };

    handleOpen = () => {
        console.log("Connected to Server");
        this.sendMessage("Fetching UI Data");
        setInterval(() => {
            this.sendMessage("Fetching UI Data");
        }, 50000);
    };

    handleClose = () => {
        console.log("Disconnected from Server");
    };

    sendMessage = (message) => {
        this.refWebSocket.sendMessage(message);
    };

    createLegend() {
        return (
            <Grid container direction="row" style={{padding: "5px", marginBottom: "5px"}}>
                <div className="ChartPage-RowBegin">
                    <div className="ChartPage-ItemTitle">Legend</div>
                </div>
                <div className="ChartPage-Row">
                    <div className="ChartPage-ItemPercentsParent">
                        <div className="ChartPage-ItemPercents"
                             style={{width: "25%", backgroundColor: "#29B6F6"}}>Mouse Usage In Min
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width: "25%", backgroundColor: "#F9A825"}}>Keyboard Usage In Min
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width: "25%", backgroundColor: "#4CAF50"}}>Idle Time In Min
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width: "25%", backgroundColor: "#f44336"}}>Open Time In Min
                        </div>
                    </div>
                </div>
            </Grid>
        );
    }

    createRow(iconName, iconURL, usagePercents) {
        return (
            <Grid container direction="row" style={{padding: "5px"}} key={iconName}>
                <div className="ChartPage-RowBegin">
                    <img style={{width: "50px", height: "50px"}}
                         src={"static/icons/" + iconURL}/>
                    <div className="ChartPage-ItemTitle">{iconName}</div>
                </div>
                <div className="ChartPage-Row">
                    <div className="ChartPage-ItemPercentsParent">
                        <div className="ChartPage-ItemPercents"
                             style={{width:  "25%", backgroundColor: "#29B6F6"}}>{usagePercents[0]}
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width: "25%", backgroundColor: "#F9A825"}}>{usagePercents[1]}
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width:  "25%", backgroundColor: "#4CAF50"}}>{usagePercents[2]}
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width: "25%", backgroundColor: "#f44336"}}>{usagePercents[3]}
                        </div>
                    </div>
                </div>
            </Grid>
        );
    }

    render() {
        // {
        // “Chrome” : {“mouse_usage”: 40, “keyboard_usage”: 30, “idle”: 10, “thinking”: 20},
        // “Visual Studio” : {“mouse_usage”: 20, “keyboard_usage”: 50, “idle”: 10, “thinking”: 20}
        // }
        return (
            <Container className="ChartPage">
                {this.createLegend()}
                <div className="ChartPage-Scroll">
                    {this.processData(this.state.data)}
                    {/*{this.createRow("Google Chrome", "https://icons.iconarchive.com/icons/google/chrome/256/Google-Chrome-icon.png", [40, 30, 10, 20])}*/}
                    {/*{this.createRow("Visual Studio", "https://cdn.iconscout.com/icon/free/png-256/visual-studio-569577.png", [20, 50, 10, 20])}*/}
                    {/*{this.createRow("PyCharm", "https://dashboard.snapcraft.io/site_media/appmedia/2017/12/PyCharmEdu256.png", [30, 40, 20, 10])}*/}
                    {/*{this.createRow("Google Chrome", "https://icons.iconarchive.com/icons/google/chrome/256/Google-Chrome-icon.png", [40, 30, 10, 20])}*/}
                    {/*{this.createRow("Visual Studio", "https://cdn.iconscout.com/icon/free/png-256/visual-studio-569577.png", [20, 50, 10, 20])}*/}
                    {/*{this.createRow("PyCharm", "https://dashboard.snapcraft.io/site_media/appmedia/2017/12/PyCharmEdu256.png", [30, 40, 20, 10])}*/}
                    {/*{this.createRow("Google Chrome", "https://icons.iconarchive.com/icons/google/chrome/256/Google-Chrome-icon.png", [40, 30, 10, 20])}*/}
                    {/*{this.createRow("Visual Studio", "https://cdn.iconscout.com/icon/free/png-256/visual-studio-569577.png", [20, 50, 10, 20])}*/}
                    {/*{this.createRow("PyCharm", "https://dashboard.snapcraft.io/site_media/appmedia/2017/12/PyCharmEdu256.png", [30, 40, 20, 10])}*/}
                </div>
                <Container className="ChartPage-UserDetails">
                    <div className="ChartPage-UserDetails-Title">
                        User Details:
                    </div>
                    <div className="ChartPage-UserDetails-Text">
                        Username: {this.state.network['username']}
                    </div>
                    <div className="ChartPage-UserDetails-Text">
                        Home Directory: {this.state.network['homedir']}
                    </div>
                    <div className="ChartPage-UserDetails-Text">
                        Wifi SSID: {this.state.network['wifi_info']}
                    </div>
                    <div className="ChartPage-UserDetails-Text">
                        Hostname: {this.state.network['hostname']}
                    </div>
                    <div className="ChartPage-UserDetails-Text">
                        IP Address: {this.state.network['ip_address']}
                    </div>
                    <div className="ChartPage-UserDetails-Text">
                        Mac Address: {this.state.network['mac_address']}
                    </div>
                </Container>
                {/*<button onClick={() => this.sendMessage("Hello World!")}>Send Message</button>*/}
                <WebSocketWrapper
                    url={this.SERVER_URL} onMessage={this.handleData}
                    onOpen={this.handleOpen} onClose={this.handleClose}
                    reconnect={true} debug={true}
                    ref={Websocket => {
                        this.refWebSocket = Websocket;
                    }}/>
            </Container>
        );
    }
}

export default ChartPage;