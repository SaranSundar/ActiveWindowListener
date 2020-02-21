import React, {Component} from 'react';
import { 
    Button,
    Container,
    Row,
    Col
 } from 'react-bootstrap';
import PieChart from '../PieChart/PieChart'
import './ChartPage.css';
import 'bootstrap/dist/css/bootstrap.min.css';

var application_data = {
    "Chrome": {
        mouse_usage: 40, 
        keyboard_usage: 30, 
        idle: 10, 
        thinking: 20
    },
    "Visual Studio": {
        mouse_usage: 20, 
        keyboard_usage: 50, 
        idle: 10, 
        thinking: 20
    },
    "Visual Studio Code": {
        mouse_usage: 20, 
        keyboard_usage: 50, 
        idle: 10, 
        thinking: 20
    },
    "Microsoft Word": {
        mouse_usage: 20, 
        keyboard_usage: 50, 
        idle: 10, 
        thinking: 20
    }
}

var user_data = {
    "wifi_info": "wifi info",
    "username": "user name",
    "homedir": "/user/home/dir",
    "alt_homedir": "/alt/home/dir",
    "hostname": "host name",
    "ip_address": "127:000:000",
    "mac_address": "MAC ADD",
    "formatted_mac_address": "FOMATTED MAC ADD",
    "hostname_by_address": "HOST NAME"
}

class ChartPage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="ChartPage">
                <div className="time-breakdown">
                    <Container>
                        <Row>
                            <Col>
                                <h2>Time Breakdown</h2>
                                <PieChart data={application_data}></PieChart>
                            </Col>
                        </Row>
                    </Container>
                </div>
                <div className="user-details">
                    <Container>
                        <Row>
                            <Col>
                                <h2>Most Recent</h2>
                            </Col>
                            <Col>
                                <h2>User Stats</h2>
                                { Object.keys(user_data).map((value, key) => {
                                    return <p>{ value } : { user_data[value] }</p>
                                }) }
                            </Col>
                        </Row>
                    </Container>
                </div>
            </div>
        );
    }
}

export default ChartPage;