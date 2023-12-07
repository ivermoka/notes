<template>
  <div class="mx-10">
    <button @click="addNote" class="mb-4 mr-5">Add note</button>
    <button>Sync with others</button>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4 reversed-cols">
      <note @push="(n) => noteValue = n" :notes="notes" :data="data[index]" v-if="notes.length > 0" v-for="(note, index) in notes" :key="index" />
      <p v-else>No notes yet..</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import Note from './components/Note.vue'
import {onMounted, ref, watch} from 'vue'

interface NoteType {
  id: number;
  title: string;
  text: string;
  timestamp: number;
}

const notes = ref<NoteType[]>([])
const data = ref<NoteType[]>([])
const noteValue = ref<object>({})
const addNote = () => {
  const note = {
    id: notes.value.length + 1,
    title: "",
    text: "",
    timestamp: Date.now()
  }
  notes.value.push(note)
}
const syncNotes = async () => {
  try {
    const response = await fetch("http://localhost:5000/");
    if (!response.ok) {
      console.error(`Request failed with status ${response.status}: ${response.statusText}`);
    }
    data.value = await response.json();
  } catch (error) {
    console.error("An error occurred while fetching data:", error);
  }
}
watch(noteValue, async (value)  => {
  console.log(value)
  const response = await fetch("http://localhost:5000/push", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(value),
  });

})

onMounted(async () => {
  await syncNotes();
  notes.value = data.value
})
</script>