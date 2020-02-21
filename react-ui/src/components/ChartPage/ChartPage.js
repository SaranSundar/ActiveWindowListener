import React, {Component} from 'react';
import './ChartPage.css';
import Grid from '@material-ui/core/Grid';
import Container from "@material-ui/core/Container";

class ChartPage extends Component {
    constructor(props) {
        super(props);
    }

    createRow(iconName, iconURL, usagePercents) {
        return (
            <Grid container direction="row" style={{padding: "5px"}}>
                <div className="ChartPage-RowBegin">
                    <img style={{width: "50px", height: "50px"}}
                         src={iconURL}/>
                    <div className="ChartPage-ItemTitle">{iconName}</div>
                </div>
                <div className="ChartPage-Row">
                    <div className="ChartPage-ItemPercentsParent">
                        <div className="ChartPage-ItemPercents"
                             style={{width: usagePercents[0] + "%", backgroundColor: "#29B6F6"}}>MU {usagePercents[0]}%
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width: usagePercents[1] + "%", backgroundColor: "#F9A825"}}>KU {usagePercents[1]}%
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width: usagePercents[2] + "%", backgroundColor: "#4CAF50"}}>IT {usagePercents[2]}%
                        </div>
                        <div className="ChartPage-ItemPercents"
                             style={{width: usagePercents[3] + "%", backgroundColor: "#f44336"}}>TT {usagePercents[3]}%
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
                <div className="ChartPage-Scroll">
                    {this.createRow("Google Chrome", "https://icons.iconarchive.com/icons/google/chrome/256/Google-Chrome-icon.png", [40, 30, 10, 20])}
                    {this.createRow("Visual Studio", "https://cdn.iconscout.com/icon/free/png-256/visual-studio-569577.png", [20, 50, 10, 20])}
                    {this.createRow("PyCharm", "https://dashboard.snapcraft.io/site_media/appmedia/2017/12/PyCharmEdu256.png", [30, 40, 20, 10])}
                    {this.createRow("Google Chrome", "https://icons.iconarchive.com/icons/google/chrome/256/Google-Chrome-icon.png", [40, 30, 10, 20])}
                    {this.createRow("Visual Studio", "https://cdn.iconscout.com/icon/free/png-256/visual-studio-569577.png", [20, 50, 10, 20])}
                    {this.createRow("PyCharm", "https://dashboard.snapcraft.io/site_media/appmedia/2017/12/PyCharmEdu256.png", [30, 40, 20, 10])}
                    {this.createRow("Google Chrome", "https://icons.iconarchive.com/icons/google/chrome/256/Google-Chrome-icon.png", [40, 30, 10, 20])}
                    {this.createRow("Visual Studio", "https://cdn.iconscout.com/icon/free/png-256/visual-studio-569577.png", [20, 50, 10, 20])}
                    {this.createRow("PyCharm", "https://dashboard.snapcraft.io/site_media/appmedia/2017/12/PyCharmEdu256.png", [30, 40, 20, 10])}
                </div>
                <Container>
                    <div>
                        User Details:
                    </div>
                </Container>
            </Container>
        );
    }
}

export default ChartPage;