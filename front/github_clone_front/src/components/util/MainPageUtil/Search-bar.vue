<template>
  <div>
    <button @click="openPopup" id="id-open-popup"><i class="bi bi-search"></i> &nbsp; {{searchQuery}}</button>
    <div v-if="isPopupOpen" class="popup-overlay" @click="closePopup">
      <div class="popup" @click.stop>
        <div class="search-bar-popup">
            &#160;<i class="bi bi-search"></i>
            <input v-model="searchQuery" type="text" id="id-search-input" @keyup.enter="search">
        </div>
        <div class="popup-content">
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isPopupOpen: false,
      searchQuery: ''
    };
  },
  methods: {
    openPopup() {
      this.isPopupOpen = true;
    },
    closePopup() {
      this.isPopupOpen = false;
    },
    search() {
      if (this.searchQuery.trim() !== '') {
        this.$router.push({ path: '/search', query: { q: this.searchQuery } });
        this.closePopup();
      }
    }
  },
  created() {
    const query = this.$route.query.q;
    if (query) {
      this.searchQuery += query;
    }
  }
};
</script>

<style scoped>
#id-open-popup {
    background: none;
    border: 1px solid rgb(152, 152, 152);
    width: 100%;
    text-align: left;
    color: white;
}

#id-search-input {
    background: none;
    border: none;
    width: 96%;
    outline: none;
    color: white;
    margin-left: 10px;
}

.search-bar-popup{
    border: 3px solid rgb(9, 67, 193);
    border-radius: 5px;
    padding: 5px;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start; /* Align to the top */
  justify-content: center;
}

.popup {
  background: #24292e;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  margin-inline-end: 5.5rem;
  margin-inline-start: 5.5rem;
  margin-top: 0.5rem;
}
</style>
