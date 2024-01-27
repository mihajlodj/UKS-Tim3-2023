<template>
  <div>
    <button @click="openPopup" id="id-open-popup"><i class="bi bi-search"></i></button>
    <div v-if="isPopupOpen" class="popup-overlay" @click="closePopup">
      <div class="popup" @click.stop>
        <input v-model="searchQuery" type="text" placeholder="Search...">
        <!-- Your popup content goes here -->
        <div>
          <!-- Popup content goes here -->
        </div>
        <button @click="closePopup">Close Popup</button>
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
    }
  }
};
</script>

<style scoped>
#id-open-popup {
    background: none;
    border: 1px solid rgb(152, 152, 152);
    width: 15rem;
    text-align: left;
    color: white;
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
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 100%; /* Stretch across the entire width */
  max-width: 400px;
}

/* Add your styles for the search bar and other popup content here */
</style>
