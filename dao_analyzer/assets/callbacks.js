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
        },
        share_click: function(n_clicks, url) {
            // Returns dialog classList
            console.log("Clicked");
            console.log(n_clicks);
            console.log(dismiss_click);

            if (n_clicks == undefined) return false;

            console.log(url);

            if (navigator.share) {
                navigator.share({
                    title: 'Share this DAO',
                    url: url
                }).then(() => {
                    console.log('Thanks for sharing!');
                }).catch(console.error);

                return false
            } else {
                console.log("Inside the else");

                setTimeout(function() {
                    console.log("Deleting the popover");
                    // document.getElementById('daohaus-organization-share-popover').display = none;
                }, 2000);

                console.log("Showing the popover");
                return true
            }
        }
    }
});