<template>
  <div class="entire-page">
    <nav-bar/>
    <div class="container pt-4">
      <h3 class="mb-4 text-light">Event History</h3>
      <div v-if="events.length === 0" class="alert alert-info">
        No events found.
      </div>
      <div v-else>
        <div v-for="(event, index) in events" :key="index" class="card mb-3">
          <div class="card-body card-class">
            <p class="card-text">{{ event.text }}</p>
            <p class="card-text"><small class="text-muted">{{ formatDate(event.time) }}</small></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
import NavBar from '../util/MainPageUtil/Nav-bar.vue';

export default {
  name: 'EventHistoryPage',
  components: {
    NavBar
  },
  data() {
    return {
      events: [],
    };
  },
  methods: {
    fetchEventHistory() {
      const { username, repoName, id, type } = this.$route.params;
      RepositoryService.getEventHistory(username, repoName, id, type).then((res) => {
        console.log(res.data);
        this.events = res.data;
      });
    },
    formatDate(dateTime) {
      const formattedDate = new Date(dateTime).toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      });
      return formattedDate;
    }
  },
  mounted() {
    this.fetchEventHistory();
  },
};
</script>

<style scoped>
.card-class {
  background: rgb(130, 153, 170);
}

.entire-page {
  min-height: 100vh;
  margin: 0px;
  padding: 0;
  background: #24292e;
}
</style>
