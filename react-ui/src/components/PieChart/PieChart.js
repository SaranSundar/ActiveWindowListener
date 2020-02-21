import React, {Component} from 'react';
import {HorizontalBar} from 'react-chartjs-2';
import './PieChart.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const options = {
  scales: {
       xAxes: [{
           stacked: true
       }],
       yAxes: [{
           stacked: true
       }]
   }
}

const colors = {
  "mouse_usage": "#03A9F4",
  "keyboard_usage": "#009688",
  "idle": "#FFEB3B",
  "thinking": "#9C27B0"
}

class PieChart extends Component {
    constructor(props) {
      super(props);
    }

    render() {
      const data = {
        labels: [],
        datasets: []
      };

      var counter = 0;
      var data_pack = {
            
      }
      // Follows the assumption that an app will NEVER duplicate
      Object.keys(this.props.data).forEach((app) => {
        Object.keys(this.props.data[app]).forEach((usage) => { 
          data_pack[usage] = {
            // stack: counter++,
            label: usage,
            data: [],
            backgroundColor: colors[usage],
            hoverBackgroundColor: "rgba(55, 160, 225, 0.7)",
						hoverBorderWidth: 2,
						hoverBorderColor: 'lightgrey'
          };
        })
      })

      // Follows the assumption that an app will NEVER duplicate
      Object.keys(this.props.data).forEach((app) => {
        data.labels.push(app);

        Object.keys(this.props.data[app]).forEach((usage) => {
          data_pack[usage].data.push(this.props.data[app][usage]);
          // data.datasets.push(new_data);
        })

        Object.keys(data_pack).forEach((usage) => {
          data.datasets.push(data_pack[usage])
        });

        console.log(data_pack)
      })

      console.log(data);

      return (
        <HorizontalBar data={data} options={options}/>
      );
    }
}

export default PieChart;