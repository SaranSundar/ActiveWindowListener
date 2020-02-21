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
    Chrome: {
        mouse_usage: 40, 
        keyboard_usage: 30, 
        idle: 10, 
        thinking: 20
    },
    Visual_Studio: {
        mouse_usage: 20, 
        keyboard_usage: 50, 
        idle: 10, 
        thinking: 20
    }
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
                                <PieChart></PieChart>
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
                            </Col>
                        </Row>
                    </Container>
                </div>
            </div>
        );
    }
}

export default ChartPage;