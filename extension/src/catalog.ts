
export interface CatalogQuery {
  vendor?: string;
  minInputTokens?: number;
}

export interface ModelLike {
  name?: unknown;
  id?: unknown;
  vendor?: unknown;
  family?: unknown;
  version?: unknown;
  maxInputTokens?: unknown;
}

export interface CatalogModel {
  name: string | null;
  id: string | null;
  vendor: string | null;
  family: string | null;
  version: string | null;
  maxInputTokens: number | null;
}

function stringOrNull(value: unknown): string | null {
  return typeof value === 'string' && value.length > 0 ? value : null;
}

function numberOrNull(value: unknown): number | null {
  return typeof value === 'number' && Number.isFinite(value) ? value : null;
}

export function normalizeCatalog(models: readonly ModelLike[], query: CatalogQuery = {}): CatalogModel[] {
  const min = typeof query.minInputTokens === 'number' && Number.isFinite(query.minInputTokens)
    ? Math.max(0, query.minInputTokens)
    : 0;
  const vendor = typeof query.vendor === 'string' && query.vendor.length > 0 ? query.vendor : undefined;

  return models
    .map((model): CatalogModel => ({
      name: stringOrNull(model.name),
      id: stringOrNull(model.id),
      vendor: stringOrNull(model.vendor),
      family: stringOrNull(model.family),
      version: stringOrNull(model.version),
      maxInputTokens: numberOrNull(model.maxInputTokens),
    }))
    .filter((model) => !vendor || model.vendor === vendor)
    .filter((model) => min === 0 || (model.maxInputTokens !== null && model.maxInputTokens >= min))
    .sort((a, b) => {
      const ak = `${a.vendor ?? ''}:${a.name ?? ''}:${a.id ?? ''}`;
      const bk = `${b.vendor ?? ''}:${b.name ?? ''}:${b.id ?? ''}`;
      return ak.localeCompare(bk);
    });
}
