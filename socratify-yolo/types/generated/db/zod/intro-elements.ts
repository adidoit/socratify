import { z } from "zod";
import { ChartConfigSchema } from "./chart-config";

const ZoomOutTextQuoteSchema = z.object({
  text: z.string(),
  source: z.string(),
});

const EntityExplainerSchema = z.object({
  title: z.string(),
  text: z.string(),
  imageUrl: z.string(),
  chartConfig: ChartConfigSchema,
});

const SituationExplainerSchema = z.object({
  title: z.string(),
  text: z.string(),
  imageUrl: z.string(),
  zoomOutTextQuote: ZoomOutTextQuoteSchema,
});

const QuestionSchema = z.object({
  id: z.string(),
  text: z.string(),
  answer: z.string(),
  type: z.enum(["quick", "deep"]),
});

export const IntroElementsSchema = z.object({
  entityExplainer: EntityExplainerSchema,
  situationExplainer: SituationExplainerSchema,
  questions: z.array(QuestionSchema),
});

export type IntroElements = z.infer<typeof IntroElementsSchema>;
