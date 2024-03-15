new Vue({
    el: '#app',
    data: {
      query: '',
      latitude: null,
      longitude: null,
      response: ''
    },
    methods: {
      getLocation() {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            position => {
              this.latitude = position.coords.latitude;
              this.longitude = position.coords.longitude;
            },
            error => {
              console.error('Error getting location:', error);
            }
          );
        } else {
          console.error('Geolocation is not supported by this browser.');
        }
      },
      submitQuery() {
        if (this.latitude && this.longitude) {
          axios.post('http://localhost:5000/query', {
            query: this.query,
            latitude: this.latitude,
            longitude: this.longitude
          })
          .then(response => {
            this.response = response.data.response;
          })
          .catch(error => {
            console.error(error);
          });
        } else {
          console.error('Latitude and longitude are not available.');
        }
      }
    },
    mounted() {
      this.getLocation();
    }
  });