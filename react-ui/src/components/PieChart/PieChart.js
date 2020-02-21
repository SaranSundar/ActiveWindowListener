import React, {Component} from 'react';
import {Pie} from 'react-chartjs-2';
import './PieChart.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const data = {
	labels: [
		'Chrome',
		'Word',
		'Terminal'
	],
	datasets: [{
		data: [300, 50, 100],
		backgroundColor: [
		'#FF6384',
		'#36A2EB',
		'#FFCE56'
		],
		hoverBackgroundColor: [
		'#FF6384',
		'#36A2EB',
		'#FFCE56'
		]
	}]
};

class PieChart extends Component {
    constructor(props) {
      super(props);
    }

    render() {
      return (
        <Pie data={data} />
      );
    }
}

export default PieChart;