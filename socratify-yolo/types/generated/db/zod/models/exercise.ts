import { z } from 'zod';
import { CoverElementsSchema } from '../cover-elements';
import { IntroElementsSchema } from '../intro-elements';
import { ImplicationQuestionSchema } from '../implication-question';
import { MentalModelSchema } from '../mental-model';
import { KeyQuestionSchema } from '../key-question';
import { MetaDataSchema } from '../meta-data';

export const ExerciseModelSchema = z.object({
  id: z.number().int(),
  exerciseVersion: z.number().int(),
  exerciseUuid: z.string(),
  exerciseType: z.string(),
  storyType: z.string(),
  coverElements: CoverElementsSchema,
  introElements: IntroElementsSchema,
  implicationQuestion: ImplicationQuestionSchema,
  mentalModel: MentalModelSchema,
  context: z.string(),
  keyQuestion: KeyQuestionSchema,
  status: z.string(),
  createdAt: z.date(),
  updatedAt: z.date(),
  tags: z.string(),
  metaData: MetaDataSchema,
  skills: z.any(),
});
