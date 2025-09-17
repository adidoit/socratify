import { z } from 'zod';

export const ChartMetadataSchema = z.object({
  valueType: z.enum(['currency', 'percentage', 'count', 'ratio', 'decimal']),
  currencyCode: z.enum(['USD', 'EUR', 'GBP', 'JPY']).optional(),
});

export const BaseChartSchema = z.object({
  archetype: z.enum([
    'kpi-metric',
    'time-series',
    'bar-chart',
    'sparkline-widget',
    'multi-line-comparison',
    'area-history',
    'minibar-comparison',
  ]),
  title: z.string().min(5).max(30),
  subtitle: z.string().min(3).max(40).optional(),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
  source: z.string().optional(),
  features: z.array(z.string()),
  metadata: ChartMetadataSchema.optional(),
});

export const KPIMetricChartSchema = BaseChartSchema.extend({
  archetype: z.literal('kpi-metric'),
  metadata: ChartMetadataSchema,
  data: z.object({
    value: z.number(),
    change: z.number(),
    changeValue: z.number(),
    trend: z.enum(['up', 'down', 'flat']),
    insight: z.string().min(10).max(50),
  }),
});

export const TimeSeriesChartSchema = BaseChartSchema.extend({
  archetype: z.literal('time-series'),
  metadata: ChartMetadataSchema,
  data: z.object({
    points: z
      .array(
        z.object({
          date: z.string(),
          value: z.number(),
        })
      )
      .min(1)
      .max(12),
    currentValue: z.number(),
  }),
});

export const BarChartSchema = BaseChartSchema.extend({
  archetype: z.literal('bar-chart'),
  metadata: ChartMetadataSchema,
  data: z.object({
    bars: z
      .array(
        z.object({
          label: z.string().max(10),
          value: z.number(),
        })
      )
      .min(3)
      .max(5),
  }),
});

export const SparklineChartSchema = BaseChartSchema.extend({
  archetype: z.literal('sparkline-widget'),
  symbol: z.string().min(2).max(10),
  metadata: ChartMetadataSchema,
  data: z.object({
    symbol: z.string(),
    history: z.array(z.number()).min(3).max(30),
    current: z.number(),
    change: z.number(),
    changePercent: z.number(),
    startDate: z.string().min(3).max(20),
    endDate: z.string().min(3).max(20),
    insight: z.string().min(5).max(30),
  }),
});

export const MultiLineChartSchema = BaseChartSchema.extend({
  archetype: z.literal('multi-line-comparison'),
  data: z.object({
    series: z.tuple([
      z.object({
        name: z.string(),
        color: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
        valueType: z.enum(['currency', 'percentage', 'count', 'ratio', 'decimal']),
        points: z.array(
          z.object({
            year: z.number(),
            value: z.number(),
          })
        ),
      }),
      z.object({
        name: z.string(),
        color: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
        valueType: z.enum(['currency', 'percentage', 'count', 'ratio', 'decimal']),
        points: z.array(
          z.object({
            year: z.number(),
            value: z.number(),
          })
        ),
      }),
    ]),
  }),
});

export const AreaHistoryChartSchema = BaseChartSchema.extend({
  archetype: z.literal('area-history'),
  metadata: ChartMetadataSchema,
  data: z.object({
    trend: z
      .array(
        z.object({
          year: z.number(),
          value: z.number(),
        })
      )
      .min(5)
      .max(20),
    peakValue: z.number(),
  }),
});

export const MinibarChartSchema = BaseChartSchema.extend({
  archetype: z.literal('minibar-comparison'),
  metadata: ChartMetadataSchema,
  data: z.object({
    items: z.tuple([
      z.object({
        label: z.string(),
        value: z.number(),
        color: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      }),
      z.object({
        label: z.string(),
        value: z.number(),
        color: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
      }),
    ]),
    changePercent: z.number(),
    changeValue: z.number(),
  }),
});

export const ChartConfigSchema = z.discriminatedUnion('archetype', [
  KPIMetricChartSchema,
  TimeSeriesChartSchema,
  BarChartSchema,
  SparklineChartSchema,
  MultiLineChartSchema,
  AreaHistoryChartSchema,
  MinibarChartSchema,
]);

export type ChartConfig = z.infer<typeof ChartConfigSchema>;
export type ChartMetadata = z.infer<typeof ChartMetadataSchema>;
export type KPIMetricChart = z.infer<typeof KPIMetricChartSchema>;
export type TimeSeriesChart = z.infer<typeof TimeSeriesChartSchema>;
export type BarChart = z.infer<typeof BarChartSchema>;
export type SparklineChart = z.infer<typeof SparklineChartSchema>;
export type MultiLineChart = z.infer<typeof MultiLineChartSchema>;
export type AreaHistoryChart = z.infer<typeof AreaHistoryChartSchema>;
export type MinibarChart = z.infer<typeof MinibarChartSchema>;

