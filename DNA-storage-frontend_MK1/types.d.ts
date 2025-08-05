/// <reference types="react" />
/// <reference types="next" />

declare namespace JSX {
    interface IntrinsicElements {
        [elemName: string]: any;
    }
}

declare module 'next' {
    export interface Metadata {
        title?: string;
        description?: string;
    }
} 