<script setup lang="ts">
import CampaignCard from './CampaignCard.vue'
import type { Campaign } from '@/services/campaigns'

interface Props {
  campaigns: Campaign[]
}

interface Emits {
  (e: 'delete', id: number): void
  (e: 'edit', campaign: Campaign): void
}

defineProps<Props>()
defineEmits<Emits>()
</script>

<template>
  <div class="campaigns-grid">
    <CampaignCard
      v-for="campaign in campaigns"
      :key="campaign.id"
      :campaign="campaign"
      @delete="$emit('delete', $event)"
      @edit="$emit('edit', $event)"
    />
  </div>
</template>

<style scoped>
.campaigns-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .campaigns-grid {
    grid-template-columns: 1fr;
  }
}
</style>