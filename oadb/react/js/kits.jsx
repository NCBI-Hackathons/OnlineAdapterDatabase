import React from 'react';
import Form from 'react-jsonschema-form';
import axios from 'axios';


const constSchema = {
	title: "Todo",
	type: "object",
	required: ["title"],
	properties: {
		title: { type: "string", title: "Title", default: "A new task"},
		done: { type: "boolean", title: "Done?", default: false }
	}
};

const log = (type) => console.log.bind(console, type);


export class KitForm extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      schema: {},
      preschema: ''
    };
  }

  setSchema(res) {
    this.setState({
      schema: res,
      preschema: JSON.stringify(res, null, 2)
    });
  }

  componentDidMount() {
    axios.get('/api/schema/?format=openapi').then(res => {
      var operation = res.data.paths['/api/kit/']['post'];
      var newschema = operation.parameters[0].schema;
      this.setSchema(newschema);
    });
  }

  render() {
    return (
    	<div>
    		<Form schema={this.state.schema}
    					onChange={log("changed")}
    					onSubmit={log("submitted")}
    					onError={log("errors")} />
            <h4>JSON Schema:</h4>
            <pre>{this.state.preschema}</pre>
    	</div>
    )
  }
}
