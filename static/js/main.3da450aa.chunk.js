(this["webpackJsonpreact-ui"]=this["webpackJsonpreact-ui"]||[]).push([[0],{25:function(e,t,n){e.exports=n(41)},30:function(e,t,n){},31:function(e,t,n){},32:function(e,t,n){},33:function(e,t,n){},34:function(e,t,n){},35:function(e,t,n){},41:function(e,t,n){"use strict";n.r(t);var o=n(0),a=n.n(o),c=n(22),s=n.n(c);n(30),Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));n(31);var r=n(13),l=n(8),i=n(4),u=n(9),p=n(10),h=n(11),m=(n(32),n(12)),d=function(e){function t(e){var n;return Object(l.a)(this,t),(n=Object(u.a)(this,Object(p.a)(t).call(this,e))).state={ws:new WebSocket(n.props.url,n.props.protocol),attempts:1},n.sendMessage=n.sendMessage.bind(Object(m.a)(n)),n.setupWebsocket=n.setupWebsocket.bind(Object(m.a)(n)),n}return Object(h.a)(t,e),Object(i.a)(t,[{key:"logging",value:function(e){!0===this.props.debug&&console.log(e)}},{key:"generateInterval",value:function(e){return this.props.reconnectIntervalInMilliSeconds>0?this.props.reconnectIntervalInMilliSeconds:1e3*Math.min(30,Math.pow(2,e)-1)}},{key:"setupWebsocket",value:function(){var e=this,t=this.state.ws;t.onopen=function(){e.logging("Websocket connected"),"function"===typeof e.props.onOpen&&e.props.onOpen()},t.onmessage=function(t){console.log(t.data),e.props.onMessage(t.data)},this.shouldReconnect=this.props.reconnect,t.onclose=function(){if(e.logging("Websocket disconnected"),"function"===typeof e.props.onClose&&e.props.onClose(),e.shouldReconnect){var t=e.generateInterval(e.state.attempts);e.timeoutID=setTimeout((function(){e.setState({attempts:e.state.attempts+1}),e.setState({ws:new WebSocket(e.props.url,e.props.protocol)}),e.setupWebsocket()}),t)}},t.onerror=function(n){console.log("++++++++++++++++++"),console.log("ERROR WS: ",t.readyState),console.log(e.props.url),console.log("++++++++++++++++++")}}},{key:"componentDidMount",value:function(){this.setupWebsocket()}},{key:"componentWillUnmount",value:function(){this.shouldReconnect=!1,clearTimeout(this.timeoutID),this.state.ws.close()}},{key:"sendMessage",value:function(e){var t=this.state.ws;e=JSON.stringify(e),t.send(e)}},{key:"render",value:function(){return a.a.createElement(o.Fragment,null)}}]),t}(a.a.Component);d.defaultProps={debug:!1,reconnect:!0};var f=d,g=function(e){function t(e){var n;return Object(l.a)(this,t),(n=Object(u.a)(this,Object(p.a)(t).call(this,e))).handleData=function(e){console.log("Data received"),console.log(e)},n.handleOpen=function(){console.log("Connected to Server")},n.handleClose=function(){console.log("Disconnected from Server")},n.sendMessage=function(e){n.refWebSocket.sendMessage(e)},n.SERVER_URL="ws://localhost:43968/example_ws/echo-example",n}return Object(h.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){var e=this;return a.a.createElement("div",{className:"WebSocketExample"},a.a.createElement("button",{onClick:function(){return e.sendMessage("Hello World!")}},"Send Message"),a.a.createElement(f,{url:this.SERVER_URL,onMessage:this.handleData,onOpen:this.handleOpen,onClose:this.handleClose,reconnect:!0,debug:!0,ref:function(t){e.refWebSocket=t}}))}}]),t}(a.a.Component);n(33);var b=function(){return a.a.createElement("div",{className:"NoMatch"},"Sorry, this page doesn't exist. Click Here to Go Back Home.")},v=n(50),O=(n(34),function(e){function t(e){return Object(l.a)(this,t),Object(u.a)(this,Object(p.a)(t).call(this,e))}return Object(h.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return a.a.createElement("div",{className:"Home"},"HOME PAGE")}}]),t}(o.Component)),k=(n(35),function(e){function t(e){return Object(l.a)(this,t),Object(u.a)(this,Object(p.a)(t).call(this,e))}return Object(h.a)(t,e),Object(i.a)(t,[{key:"render",value:function(){return a.a.createElement("div",{className:"ChartPage"},"Chart Page")}}]),t}(o.Component));var E=function(){return a.a.createElement(o.Fragment,null,a.a.createElement(v.a,null),a.a.createElement("div",{className:"App"},a.a.createElement(r.c,null,a.a.createElement(r.a,{exact:!0,path:"/",component:k}),a.a.createElement(r.a,{exact:!0,path:"/home",component:O}),a.a.createElement(r.a,{exact:!0,path:"/example",component:g}),a.a.createElement(r.a,{component:b}))))},j=n(17);s.a.render(a.a.createElement(j.a,null,a.a.createElement(E,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[25,1,2]]]);
//# sourceMappingURL=main.3da450aa.chunk.js.map