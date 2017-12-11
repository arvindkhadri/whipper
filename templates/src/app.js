import _ from 'lodash';
import React from 'react';
import ReactDOM from 'react-dom';
import Bootstrap from 'bootstrap/dist/css/bootstrap.css';


class CurrentImages extends React.Component {
    constructor (props) {
        super(props);
    }

    componentDidUpdate () {
        this.foo.scrollIntoView();
    }

    render() {
        return (
            <div ref = { (id) => { this.foo = id; } } className="row">
                <h3> Images </h3>
                {this.props.images.map((imgUrl, idx) => { 
                    return (<div className="col-sm-4"><img className="img-thumbnail" key={idx} src={imgUrl}></img></div>);
                 })
                }
            </div>
        );
    }
}


class AppView extends React.Component {
    constructor (props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        const tagsMapKeys = props.data.reduce((acc, o) => { 
        // Build an object where the key is the tagname, and value is an array of
        // urls for that tag.
            Object.entries(o).forEach(([k,v]) => { 
                v.forEach(vi => acc[vi] = (acc[vi] || []).concat(k)) 
            }); 
            return acc; 
        }, {});

        this.state = {
            currentImages: [],
            transformed: _.map(tagsMapKeys, (i, idx) => {
                return (
                    <li style={{cursor: 'pointer'}} onClick={(e) => this.handleClick(e)}>{idx}</li>
                );
            }),
            tagsMapKeys
        };
    }

    handleClick(e) {
        const tag = e.target.textContent;
        this.setState({currentImages: this.state.tagsMapKeys[tag]});
    }

    render() {
        return (
                <div className="row">
                    <div className="col-md-4">
                        <ul> <h3>Tags:</h3>
                            {this.state.transformed}
                        </ul>
                    </div>

                    <div className="col-md-8">
                        <CurrentImages images={this.state.currentImages} />
                    </div>    
                </div>
        );

    }
}


ReactDOM.render(
  <AppView data={window.response}/> ,
  document.getElementById('root')
);

