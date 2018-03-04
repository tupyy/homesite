function parse_next_url(url) {
    if ( url.search("next=") ) {
        return url.substr(url.search("=")+1);
    }
}