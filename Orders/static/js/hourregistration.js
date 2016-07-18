var HourRegistrationComponent = React.createClass({
    componentDidMount: function() {
        $.ajax('/')
    },
    render: function() {
        return (
            <div>
                <p>Kies een opdracht uit de lijst en klik op <b>Start</b> om de tijd bij te houden. Klik op <b>Stop</b> als u klaar bent of pauze neemt.</p>
                <div id="article-list-select">
                    <ArticleListComponent url="/opdracht/list-hourregistration/" />
                </div>
                <ButtonComponent action="Start" />
            </div>
        );
    }
});

var ArticleListComponent = React.createClass({
    getInitialState: function () {
      return {data: [], selectedValue: 0}
    },
    componentDidMount: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function(data) {
                this.setState({data: data});;
                $('select').material_select();
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, erro.toString());
            }.bind(this)
        })
    },
    handleChange: function(e) {
        this.setState({selectedValue: e.target.value})
    },
   render: function () {
       var listNodes = this.state.data.map(function(order) {
        return (
            <ListComponent pk={order.pk} title={order.fields.title} />
        )
       }.bind(this));
       return (
           <select onChange={this.handleChange}>
               {listNodes}
           </select>
       );
   }
});

var ListComponent = React.createClass({
    render: function() {
        return (
            <option value={this.props.pk}>{this.props.title}</option>
        )
    }
});

var TimingComponent = React.createClass({
    render: function() {
        return (
            <div>
                <ul>
                    <li>U werkt nu aan: <b>{this.props.title}</b></li>
                    <li>Gestart op: <b>{this.props.start}</b></li>
                </ul>
            </div>
        );
    }
});


var ButtonComponent = React.createClass({
    getInitialState: function() {
      return {action: this.props.action}
    },
    buttonClick: function() {
        var selectedValue = $('select option:selected').val();
        var title = $('select option:selected').text();

        $.ajax({
            url: '/urenregistratie/' + this.state.action.toLowerCase() + '/' + selectedValue,
            dataType: 'json',
            success: function (data) {
                if (this.state.action == 'Start') {
                    $('#article-list-select').hide();
                    ReactDOM.render(<TimingComponent title={title}
                                                     start={data.start}/>, document.getElementById('uren-bijhouden'))
                } else {
                    $('#article-list-select').show();
                    ReactDOM.unmountComponentAtNode(document.getElementById('uren-bijhouden'))
                }
                this.setState({action: toggleStartStop(this.state.action)});
            }.bind(this),
        })
    },
    render: function() {
        return (
            <div>
                <div id="uren-bijhouden"></div>
                <button className="waves-effect waves-light btn" onClick={this.buttonClick}>{this.state.action}</button>
            </div>
        );
    }
});

function toggleStartStop(action) {
    if (action == "Start") return "Stop";
    return "Start";
}

ReactDOM.render(
    <HourRegistrationComponent />, document.getElementById('urenregistratie')
);