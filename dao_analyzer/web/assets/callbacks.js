function getDaoInfo(org) {
    // const html = window.dash_html_components;

    const grid = [];
    // const grid = [
    //     html.Div("Name", className='dao-info-label'),
    //     html.Div(org.name, className='dao-info-name'),
    //     html.Div("Network", className='dao-info-label'),
    //     html.Div(org.network, className='dao-info-network'),
    //     html.Div("Address", className='dao-info-label'),
    //     html.Div(html.Span(org.address, className='address'), className='dao-info-address'),
    // ];
    
    // return ReactDOM.render(html.Div(grid, className='dao-info-container'), null);
    return React.createElement('div', { className: 'dao-info-label'}, 'Name');
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    callbacks: {
        info_summary: function(ddvalue, orgs) {
            if ( !ddvalue ) { console.log("No dao selected"); return; }
            
            // TODO: Put in a constant instead of hardcoding
            if ( ddvalue == 1 ) { console.log("All DAOs"); return ["ALL ORGS (PH)", ] ; }
            
            console.log("Inside clientside callback");
            console.log(ddvalue);

            const org = orgs.find(e => e.address == ddvalue);
            
            console.log(org);
            // return [getDaoInfo(org), org.creation_date];
            return [getDaoInfo(org), org.creation_date]
        }
    }
});