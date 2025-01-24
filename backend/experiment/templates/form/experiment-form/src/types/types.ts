export interface TranslatedContent {
  id?: number;
  index: number;
  language: string;
  name: string;
  description: string;
  about_content: string;
  social_media_message: string;
}

export interface BlockTranslatedContent {
  index: number;
  language: string;
  name: string;
  description: string;
}

export interface BlockPlaylist {
  id: string;
  name: string;
}

export type BlockQuestionSeries = {
  id?: number;
  name: string;
  index: number;
  randomize: boolean;
  questions: string[];
}


export interface Block {
  id?: number;
  index: number;
  slug: string;
  rounds: number;
  bonus_points: number;
  rules: string;
  phase?: number;  // Make phase optional
  translated_contents: BlockTranslatedContent[];
  playlists: BlockPlaylist[];
  questionseries_set: BlockQuestionSeries[];
}

export interface Phase {
  id?: number;
  index: number;
  dashboard: boolean;
  randomize: boolean;
  blocks: Block[];
}

export interface Experiment {
  id?: number;
  slug: string;
  active: boolean;
  translated_content: TranslatedContent[];
  phases: Phase[];
}

export type Selection = {
  type: 'phase' | 'block';
  phaseIndex: number;
  blockIndex?: number;
};
